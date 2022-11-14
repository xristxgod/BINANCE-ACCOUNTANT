from typing import Optional

from flask_login import UserMixin

from ..config import login_manager


class Admin(UserMixin):
    def __init__(self, username: str, password: Optional[str] = None):
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.username


@login_manager.user_loader
def load_user(username: str):
    return Admin(username=username)

