import decimal
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
        related_name='user_crypto_wallet',
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
        verbose_name = _('Crypto Wallet')
        verbose_name_plural = _('Crypto Wallets')


class CryptoBalances(models.Model):
    amount = models.DecimalField(_('Amount'), max_digits=8, decimal_places=8, default=0)
    token = models.CharField(
        _('Token'),
        choices=enums.CryptoToken.choices,
        default=enums.CryptoToken.NATIVE
    )

    active = models.BooleanField(_('Active'), default=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_balance',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        CryptoWallet,
        related_name='crypto_wallet_balance',
        on_delete=models.SET_NULL
    )

    @property
    def balance(self) -> decimal.Decimal:
        return self.amount

    @balance.setter
    def balance(self, balance: decimal.Decimal):
        self.amount = balance

    @property
    def balance_usd(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return f'Balance: {self.pk}'

    class Meta:
        verbose_name = _('Crypto Balance')
        verbose_name_plural = _('Crypto Balances')


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

    token = models.CharField(
        _('Token'),
        choices=enums.CryptoToken.choices,
        default=enums.CryptoToken.NATIVE
    )

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        CryptoWallet,
        related_name='user_balance',
        on_delete=models.SET_NULL
    )