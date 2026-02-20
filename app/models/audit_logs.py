from app import db

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
