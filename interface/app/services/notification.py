import abc
import functools
from typing import NoReturn, Optional, Callable

import app.settings as settings


def has_default_value(default_name: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        def class_method_wrapper(cls, message: str, **kwargs):
            if getattr(cls, 'admin_' + default_name, False) and kwargs.get(default_name, False):
                return func(cls, message=message, **kwargs)
        return class_method_wrapper
    return decorator


class BaseNotification:
    @abc.abstractclassmethod
    def send(cls, message: str, **kwargs) -> NoReturn: ...


class TelegramNotification(BaseNotification):
    admin_telegram_id: Optional[int] = settings.ADMIN_TELEGRAM_ID

    @classmethod
    @has_default_value('telegram_id')
    def send(cls, message: str, telegram_id: Optional[int] = None) -> NoReturn:
        pass


class EmailNotification(BaseNotification):
    admin_email: Optional[str] = settings.ADMIN_EMAIL

    @classmethod
    @has_default_value('email')
    def send(cls, message: str, email: Optional[int] = None) -> NoReturn:
        pass


class PhoneNotification(BaseNotification):
    admin_phone_number: Optional[str] = settings.ADMIN_PHONE_NUMBER

    @classmethod
    @has_default_value('phone_number')
    def send(cls, message: str, phone_number: Optional[str] = None) -> NoReturn:
        pass


class PlatformNotification(BaseNotification):
    @classmethod
    def send(cls, message: str, **kwargs):
        pass
