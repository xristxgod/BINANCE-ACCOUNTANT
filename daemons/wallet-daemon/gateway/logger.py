import enum as e
from typing import NoReturn

import meta


class Methods(e.Enum):
    DEBUG = 'debug'
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'
    CRITICAL = 'critical'


# class GateClientLogger(meta.Logger):
#     path = 'gate_client.log'

    # @classmethod
    # def log(cls, method: Methods, message: str) -> NoReturn:
    #     getattr(cls.logger, method.value)(message)
