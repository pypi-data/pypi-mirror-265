import logging
from logging import FileHandler
from enum import Enum

class Levels(Enum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

def my_logger(name: str = 'basic', level: int | str = Levels.DEBUG.value):

    logging.basicConfig(level=level)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = FileHandler(
        filename= name,
        mode='a',
        encoding='UTF-8'
    )
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt='%(levelname)s - %(asctime)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

if __name__ == '__main__':
    logger = my_logger(name='test.log')
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warning')
    logger.critical('Prueba')

    # with open('basic.log', 'r') as f:
    #     print(f.read())