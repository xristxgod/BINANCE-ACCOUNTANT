import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.py')


DEBUG = True
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = os.getenv('SECRET_KEY', 'd5fb8c4fa8bd46638dadc4e751e0d68d')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///../database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')

ADMIN_2AF = os.getenv('ADMIN_2FA', None)
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', None)
ADMIN_TELEGRAM = os.getenv('ADMIN_TELEGRAM', None)
