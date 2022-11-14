from flask import Flask


class App:
    def __init__(self):
        self._app = Flask(__name__)
        self._setup()

    def _setup(self):
        self._set_config()
        self._set_external_app()
        self._set_views()

    def _set_config(self):
        import app.settings as settings
        self._app.config.from_pyfile(settings.SETTINGS_FILE)

    def _set_external_app(self):
        import app.config as config
        config.db.init_app(self._app)
        config.migrate.init_app(self._app)
        config.login_manager.init_app(self._app)

    def _set_views(self):
        import app.views as views
        self._app.register_blueprint(views.auth_app)
        self._app.register_blueprint(views.main_app)

    @property
    def app(self) -> Flask:
        return self._app
