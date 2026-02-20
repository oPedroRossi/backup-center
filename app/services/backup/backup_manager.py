from app.models import Device, BackupLog
from app import db


def run_all_backups():
    devices = Device.query.filter_by(backup_enabled=True).all()

    for device in devices:
        


def save_log(device_id, status, message):
    log = BackupLog(
        device_id=device_id,
        status=status,
        message=message
    )

    db.session.add(log)
    db.session.commit()
