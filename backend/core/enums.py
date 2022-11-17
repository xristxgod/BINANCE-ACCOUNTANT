from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountNetwork(models.TextChoices):
    BINANCE = 'BINANCE', _('Binance account')
    BYBIT = 'BYBIT', _('ByBit account')


class CryptoNetwork(models.TextChoices):
    TRON = 'TRON', _('Tron blockchain')


class CryptoToken(models.TextChoices):
    NATIVE = 'NATIVE', _('Native token')
    USDT = 'USDT', _('USDT token')


class TransactionType(models.IntegerChoices):
    EXTERNAL = 0, _('External transaction')
    INTERNAL = 1, _('Internal transaction')
