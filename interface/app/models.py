import enum

from sqlalchemy.sql import func

from .config import db


class NetworkEnum(enum.Enum):
    binance = 'BINANCE'
    bybit = 'BYBIT'


class AccountStatus(enum.Enum):
    error = -1
    active = 0
    inactive = 1


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    network = db.Column(db.String(10), default=NetworkEnum.binance)

    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(100), unique=True, nullable=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=True)
    active = db.Column(db.Integer, default=AccountStatus.active)

    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Account {self.name}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15))
    text = db.Column(db.String(255))

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Notification {self.title}>'
