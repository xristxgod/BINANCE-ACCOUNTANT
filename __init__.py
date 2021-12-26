# <------------------------------------------------------------------------------------------------------------------> #
from flask import Flask
from flask_login import LoginManager

from mainapp.settings import Settings, db
from mainapp.views import main
from mainapp.models import UserLogin
from mainapp.jobs import register_scheduler
# <------------------------------------------------------------------------------------------------------------------> #
def create_app(config_file=Settings):
    app = Flask(__name__)
    app.config.from_object(config_file)
    db.init_app(app)
    register_scheduler(app)
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserLogin().fromDB(user_id)

    app.register_blueprint(main)
    return app
# <------------------------------------------------------------------------------------------------------------------> #