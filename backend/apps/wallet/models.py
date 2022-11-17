from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import core.enums as enums
from core.credential_manager import WalletCredentialManager, WalletCredential


class CryptoWallet(models.Model):
    address: str = models.CharField(_('Wallet address'), max_length=255, primary_key=True, validators=[])
    network = models.CharField(
        _('Network'),
        choices=enums.CryptoNetwork.choices,
        default=enums.CryptoNetwork.TRON
    )

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_wallet',
        on_delete=models.CASCADE
    )

    @property
    def private_key(self) -> WalletCredential:
        return WalletCredentialManager.get(self.address)

    @private_key.setter
    def private_key(self, keys: WalletCredential):
        WalletCredentialManager.set(self.address, keys=keys)

    @private_key.deleter
    def private_key(self):
        WalletCredentialManager.remove(self.address)

    def __str__(self):
        return f'Wallet {self.pk} :: {self.network}'

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class CryptoExternalTransactions(models.Model):
    transaction_id = models.CharField(_('Transaction ID'), max_length=255, primary_key=True)

    address = models.CharField(_('From Wallet address'), max_length=255)

    amount = models.DecimalField(_('Amount'), max_digits=18, decimal_places=6, default=0)
    fee = models.DecimalField(_('Commission'), max_digits=18, decimal_places=6, default=0)

    network = models.CharField(
        _('Network'),
        choices=enums.CryptoNetwork.choices,
        default=enums.CryptoNetwork.TRON
    )