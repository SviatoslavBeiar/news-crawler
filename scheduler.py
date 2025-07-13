import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import fetch_and_store

logging.basicConfig(
    filename='scheduler.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

sched = BlockingScheduler()
sched.add_job(fetch_and_store, 'cron', minute='*', id='news_job')

try:
    logging.info("Scheduler started")
    sched.start()
except (KeyboardInterrupt, SystemExit):
    logging.info("Scheduler stopped")
