import os

import core.meta as meta
from mainapp.settings import LOGS_DIR


class AccountCredentialManagerLogger(meta.Logger):
    path = os.path.join(LOGS_DIR, 'account_credential_manager.log')


class WalletCredentialManagerLogger(meta.Logger):
    path = os.path.join(LOGS_DIR, 'account_credential_manager.log')
