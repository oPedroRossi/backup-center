from app import db


class Device(db.Model):
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
