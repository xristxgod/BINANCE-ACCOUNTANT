from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountNetwork(models.TextChoices):
    BINANCE = 'BINANCE', _('Binance account')
    BYBIT = 'BYBIT', _('ByBit account')
