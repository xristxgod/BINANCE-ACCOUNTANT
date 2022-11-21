import os


INTERNAL_URI = os.getenv('INTERNAL_URI', 'http://127.0.0.1:8000')
INTERNAL_LOGIN = os.getenv('INTERNAL_LOGIN', 'daemon_wallet_login')
INTERNAL_PASSWORD = os.getenv('INTERNAL_PASSWORD', 'daemon_wallet_password')

TRON_GATE = os.getenv('TRON_GATE', '')
