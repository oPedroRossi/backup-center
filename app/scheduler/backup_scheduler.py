from apscheduler.schedulers.background import BackgroundScheduler
from app.services.backup.backup_manager import run_all_backups


def start_scheduler(app):

    scheduler = BackgroundScheduler()

    def job():
        with app.app_context():
            run_all_backups()

    scheduler.add_job(
        func=job,
        trigger="cron",
        hour=2,
        minute=0
    )

    scheduler.start()
