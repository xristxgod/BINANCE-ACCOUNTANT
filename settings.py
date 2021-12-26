# <------------------------------------------------------------------------------------------------------------------> #
import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
# <------------------------------------------------------------------------------------------------------------------> #
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
# <------------------------------------------------------------------------------------------------------------------> #
class Settings(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# <------------------------------------------------------------------------------------------------------------------> #