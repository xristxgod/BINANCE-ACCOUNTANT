import decimal
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.credential_manager import WalletCredentialManager, WalletCredential


class CryptoNetwork(models.Model):
    name = models.CharField(_('Network name'), max_length=25, primary_key=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Crypto Network')
        verbose_name_plural = _('Crypto Networks')


class CryptoToken(models.Model):
    name = models.CharField(_('Token name'), max_length=25)
    symbol = models.CharField(_('Token symbol'), max_length=25)
    token_address = models.CharField(_('Token address'), default=None, null=True, blank=True, unique=True)

    decimals = models.IntegerField(_('Decimals'), default=8)
    extra = models.JSONField(_('Extra'), default=None, null=True, blank=True)

    network = models.ForeignKey(
        CryptoNetwork,
        related_name='token_network',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.network} :: {self.name}'

    class Meta:
        verbose_name = _('Crypto Token')
        verbose_name_plural = _('Crypto Token')


class CryptoWallet(models.Model):
    address: str = models.CharField(_('Wallet address'), max_length=255, primary_key=True, validators=[])
    network = models.ForeignKey(
        CryptoNetwork,
        related_name='wallet_network',
        on_delete=models.CASCADE
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
    token = models.ForeignKey(
        CryptoNetwork,
        related_name='token_network',
        on_delete=models.CASCADE
    )

    active = models.BooleanField(_('Active'), default=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_wallet_balance',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        CryptoWallet,
        related_name='wallet_balance',
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

    token = models.CharField(
        _('Token'),
        choices=enums.CryptoToken.choices,
        default=enums.CryptoToken.NATIVE
    )

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_external_transaction',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        CryptoWallet,
        related_name='wallet_crypto_external_transaction',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Balance: {self.pk}'

    class Meta:
        verbose_name = _('Crypto External Transaction')
        verbose_name_plural = _('Crypto External Transactions')