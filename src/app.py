import uvicorn
import contextlib
from loguru import logger
from typing import AsyncIterator

from routes import main_router
from loader import app, db, cfg


async def on_startup() -> None:
    await db.setup(dsn=cfg.postgres.dsn)
    logger.success("Server has started and is now running.")


async def on_shutdown():
    await db.close()
    logger.info("Database closed!")


@contextlib.asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    await on_startup()
    yield
    await on_shutdown()


if __name__ == "__main__":
    app.router.lifespan_context = lifespan
    app.include_router(main_router)

    try:
        uvicorn.run(app, host=cfg.server.host, port=cfg.server.port, log_config=None)
    except KeyboardInterrupt:
        pass
