import enum
from typing import Optional
from datetime import datetime

from flask_login import UserMixin, current_user

import meta
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
    def __init__(self):
        self.status: AdminStatus = AdminStatus.NOT_AUTH

        self.start_session: Optional[datetime] = None
        self.last_update: Optional[datetime] = None

        self._setup()

    def _setup(self):
        if current_user.is_authenticated:
            self.status = AdminStatus.AUTH
            self.start_session = datetime.now()
            self.last_update = datetime.now()

    def record(self, text: str):
        pass

    def change_status(self, status: AdminStatus):
        self.status = status
        if self.status == AdminStatus.AUTH:
            self.start_session = datetime.now()
            self.last_update = datetime.now()

            self.notification('Authorization')


@login_manager.user_loader
def load_user(username: str):
    return AdminMixin(username=username)

