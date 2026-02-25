import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from app.backups.manager import run_all_backups


def start_scheduler(app):

    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return

    scheduler = BackgroundScheduler(
        timezone=pytz.timezone("America/Sao_Paulo")
    )

    def job():
        with app.app_context():
            run_all_backups()

    scheduler.add_job(
        func=job,
        trigger="cron",
        hour=2,
        minute=0,
        id="daily_backup_job",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=3600
    )

    scheduler.start()