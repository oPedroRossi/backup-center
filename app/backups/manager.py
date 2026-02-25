#from app.backups.models import BackupLog, Device
from app.backups.vendors.sophos import sophosBackup
from app.core.extensions import db


def run_all_backups():
    devices = Device.query.filter_by(backup_enabled=True).all()

    for device in devices:
        try:
            if device.type == "sophos":
                SophosBackup(device)
                print(f"Running Sophos backup for device {device.name} ({device.ip_address})")
            save_log(device.id, "success", "Backup completed successfully.")
        except Exception as e:
            save_log(device.id, "failure", f"Backup failed: {str(e)}")

