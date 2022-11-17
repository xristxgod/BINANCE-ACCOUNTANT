import os

import core.meta as meta
from mainapp.settings import LOGS_DIR


class CredentialManagerLogger(meta.Logger):
    path = os.path.join(LOGS_DIR, 'credential_manager.log')
