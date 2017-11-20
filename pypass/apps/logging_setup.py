import os
import logging

from logging.handlers import RotatingFileHandler

from core.utils import get_timestamp

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console and file handlers and set level to debug
os.makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/flask.log',
                                   maxBytes=100000, backupCount=5)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(levelname)s [{0}] %(name)s:%(module)s.%(funcName)s -> '
    '%(message)s'.format(
        get_timestamp())
)

# add formatter to console_handler
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# werkzeug_logger = logging.getLogger('werkzeug')
# werkzeug_logger.setLevel(logging.DEBUG)
# werkzeug_logger.addHandler(console_handler)
