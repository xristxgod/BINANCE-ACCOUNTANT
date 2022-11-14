import os

import meta
import app.settings as settings


class AuthLogger(meta.Logger):
    path = os.path.join(settings.LOGS_DIR, 'auth.log')
