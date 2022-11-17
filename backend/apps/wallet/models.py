from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class WalletNetwork(models.TextChoices):
    TRON = 'TRON', _('Tron blockchain')


class Wallet(models.Model):
    address = models.CharField(_('Wallet address'), primary_key=True, validators=[])
    network = models.CharField(_('Network'), choices=AccountNetwork.choices, default=AccountNetwork.BINANCE)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_wallet',
        on_delete=models.CASCADE
    )

