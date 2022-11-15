import enum
import functools
from typing import Optional, Callable
from datetime import datetime

from flask import redirect, url_for
from flask_login import UserMixin, current_user

import meta
import app.settings as settings
import app.services.logger as logger
from ..config import login_manager


class AdminStatus(enum.Enum):
    NOT_AUTH = 0
    AUTH_2FA = 1
    AUTH = 2


class AdminMixin(UserMixin):
    def __init__(self, username: str, password: Optional[str] = None):
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.username


class AdminAuth(meta.Singleton):

    admin_2fa_code = settings.ADMIN_2AF_CODE

    def __init__(self):
        self.status: AdminStatus = AdminStatus.NOT_AUTH

        self.admin_mixin: Optional[AdminMixin] = None
        self.start_session: Optional[datetime] = None
        self.last_update: Optional[datetime] = None

        self._setup()

    def _setup(self):
        if bool(current_user) and current_user.is_authenticated:
            self.admin_mixin = AdminMixin(username=current_user.id)
            self.status = AdminStatus.AUTH
            self.start_session = datetime.now()
            self.last_update = datetime.now()

    @property
    def admin(self) -> AdminMixin:
        return self.admin_mixin

    @admin.setter
    def admin(self, value: AdminMixin):
        self.admin_mixin = value

    @classmethod
    def get_2fa_code(cls) -> int:
        import pyotp
        return int(pyotp.TOTP(cls.admin_2fa_code).now())

    def change_status(self, status: AdminStatus):
        logger.AuthLogger.log(message=f'Change status: {self.status} => {status}')
        self.status = status
        if self.status == AdminStatus.AUTH:
            self.start_session = datetime.now()
            self.last_update = datetime.now()
            logger.AuthLogger.log(message='Auth')
            # celery_app.send_task(f'worker_sender.celery_worker.send_notification', args=[text], **extra)


@login_manager.user_loader
def load_user(username: str):
    return AdminMixin(username=username)


def is_auth(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper
