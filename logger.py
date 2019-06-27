import logging.config
import os

_WORKSPACE = os.getenv('WORKSPACE', default=R'C:\opt\ci\jenkins\workspace\Killer_Automation')


def _get_named_logging_config(test_name):
    named_logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'file': {
                'format': '[%(asctime)-s] {%(filename)-30s:%(funcName)30s():%(lineno)3d} %(levelname)-8s - %(message)-s'
            },
            'console': {
                'format': '[%(asctime)-s] {%(filename)-30s:%(funcName)30s():%(lineno)3d} %(levelname)-8s - %(message)-s'
            },
        },
        handlers={
            'default': {'level': 'DEBUG', 'formatter': 'console', 'class': 'logging.StreamHandler'},
            'file': {
                'level': 'DEBUG',
                'formatter': 'file',
                'class': 'logging.FileHandler',
                'filename': fR'{_WORKSPACE}\{test_name}.log',
                'mode': 'w',
                'encoding': 'utf-8',
            },
        },
        loggers={
            '': {'handlers': ['default', 'file'], 'level': 'DEBUG', 'propagate': True},
            'hammer': {'handlers': ['default'], 'level': 'INFO', 'propagate': False},
        },
        root={'handlers': ['default', 'file'], 'level': 'DEBUG'},
    )
    return named_logging_config


def instantiate_logger(name):
    named_logging_config = _get_named_logging_config(''.join(['robot_', name]))
    return named_logging_config


def make_logging(name):
    global log
    named_logging_config = instantiate_logger(name)
    logging.config.dictConfig(named_logging_config)
    log = logging.getLogger('')


def attach_to_logger(name):
    # global log
    make_logging(name)
    log = logging.getLogger(name)
    return log