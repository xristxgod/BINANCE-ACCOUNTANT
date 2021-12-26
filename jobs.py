# <------------------------------------------------------------------------------------------------------------------> #
from flask_apscheduler import APScheduler
from mainapp.biance_script import start
# <------------------------------------------------------------------------------------------------------------------> #
def run():
    start()
# <------------------------------------------------------------------------------------------------------------------> #
def register_scheduler(app):
    ''' Adding a subtask to run at a specific time '''
    scheduler = APScheduler()
    scheduler.init_app(app)
    # This script will start its work at 3:30 Moscow time
    scheduler.add_job(id='Binance Script', func=run, trigger='cron', hour=10, minute=26)
    scheduler.start()
# <------------------------------------------------------------------------------------------------------------------> #