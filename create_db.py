from mainapp.__init__ import create_app, db

# Создание базы данных
db.create_all(app=create_app())

# В ручную добавить пользователя
''' INSERT INTO users(username, password) VALUES ('admin', 'admin'); '''

