from app import db
from datetime import datetime


class BackupLog(db.Model):
    __tablename__ = "backup_logs"

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(
        db.Integer,
        db.ForeignKey("devices.id"),
        nullable=False
    )

    status = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    device = db.relationship("Device")
