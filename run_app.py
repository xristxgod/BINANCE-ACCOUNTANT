from mainapp.__init__ import create_app

if __name__ == '__main__':
    # Запуск сайта | use_reloader=False - Отключить автоматическое обновление
    create_app().run(use_reloader=False)

