from app.core.extensions import db
from datetime import datetime

class BackupLog(db.Model): # Adicionei a classe BackupLog para registrar os logs de backup
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

class Device(db.Model): # Adicionei a classe Device para representar os dispositivos que serão gerenciados pelo sistema
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50))
    model = db.Column(db.String(100))

    ip_address = db.Column(db.String(45), nullable=False)

    last_backup = db.Column(db.DateTime)
    last_status = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Device {self.name}>"

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    device_name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    entity = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(50), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<AuditLog {self.device_name} - {self.action}>"