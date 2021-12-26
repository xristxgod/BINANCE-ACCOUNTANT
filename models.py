# <------------------------------------------------------------------------------------------------------------------> #
from mainapp.settings import db
# <------------------------------------------------------------------------------------------------------------------> #
class Users(db.Model):
    ''' Users '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<user {}>'.format(self.username)
# <------------------------------------------------------------------------------------------------------------------> #
class Accounts(db.Model):
    ''' Accounts '''

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=True)
    api_key = db.Column(db.String(300), unique=True, nullable=True)
    secret_api_key = db.Column(db.String(300), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True)
    status = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return '<account {}>'.format(self.id)
# <------------------------------------------------------------------------------------------------------------------> #
class UserLogin:
    ''' Class for authorization '''

    def fromDB(self, user_id):
        self.__user = Users.query.get(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)
# <------------------------------------------------------------------------------------------------------------------> #