import contextlib
from typing import AsyncIterator
from loguru import logger

from loader import app, db, cfg


async def on_startup():
    await db.setup(dsn=cfg.postgres.dsn)
    logger.success("Server has started and is now running.")


async def on_shutdown():
    await db.close()


@contextlib.asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    await on_startup()
    yield
    await on_shutdown()


if __name__ == "__main__":
    import uvicorn
    app.router.lifespan_context = lifespan

    try:
        uvicorn.run(app, host=cfg.server.host, port=cfg.server.port, log_config=None)
    except KeyboardInterrupt:
        pass
