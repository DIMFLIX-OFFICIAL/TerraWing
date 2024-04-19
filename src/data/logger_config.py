import datetime
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name  # Получение соответствующего уровня Loguru для записи в лог

        ##==> Формирование сообщения как в Loguru
        #########################################
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id=None, method=None)

        ##==> Отправка сообщения в loguru
        ##################################
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


##==> Конфигурация для Uvicorn, которая будет использовать Loguru
##################################################################
def setup_logging():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger.add(f"../logs/log_{current_time}.log", encoding="utf8")
    logging.basicConfig(handlers=[InterceptHandler()], level='INFO')
