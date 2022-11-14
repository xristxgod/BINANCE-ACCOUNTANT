from flask import Flask


def init_app():
    import src.config as config
    import src.settings as settings

    app = Flask(__name__)

    app.config.from_pyfile(settings)

    config.db.init_app(app)
    config.migrate.init_app(app)
    config.login_manager.init_app(app)

    return app
