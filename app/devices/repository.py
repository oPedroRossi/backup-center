import os
from app.core.extensions import db
from app.devices.models import Device, BackupLog, AuditLog
from sqlalchemy.exc import SQLAlchemyError

def create_device_service(data: dict):

    try:
        name = data.get("name")
        device_type = data.get("device_type")
        model = data.get("model")
        ip_address = data.get("ip_address")

        if not name:
            return {"error": "Nome é obrigatório"}, 400

        if not ip_address:
            return {"error": "IP é obrigatório"}, 400

        existing_name = Device.query.filter_by(name=name).first()
        if existing_name:
            return {"error": "Já existe um device com esse nome"}, 400

        new_device = Device(
            name=name,
            device_type=device_type,
            model=model,
            ip_address=ip_address,
            created_at=db.func.current_timestamp()
        )

        db.session.add(new_device)
        db.session.commit()

        return {
            "message": "Device criado com sucesso",
            "device_id": new_device.id
        }, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_backup_failed_count():
    try:
        return Device.query.filter_by(last_status="FAILED").count()
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500


def get_backup_ok_count():
    try:
        return Device.query.filter_by(last_status="OK").count()
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def create_log_entry(device_name, action, entity):
    try:
        device = Device.query.filter_by(name=device_name).first()
        if not device:
            return {"error": "Device não encontrado"}, 404

        log_entry = AuditLog(
            device_name=device.name,
            model=device.model,
            type=device.device_type,
            entity=entity,
            action=action
        )

        db.session.add(log_entry)
        db.session.commit()

        return {"message": "Log criado com sucesso"}, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_logs_device():
    try:
        logs = (
            AuditLog.query
            .order_by(AuditLog.created_at.desc())
            .limit(5)
            .all()
        )
        return [
            {
                "device_name": log.device_name,
                "model": log.model,
                "type": log.type,
                "entity": log.entity,
                "action": log.action,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def get_equipament(device_type):
    try:
        devices = Device.query.filter_by(device_type=device_type).all()
        return [
            {
                "id": device.id,
                "name": device.name,
                "device_type": device.device_type,
                "model": device.model,
                "ip_address": device.ip_address,
                "last_status": device.last_status,
                "last_backup": device.last_backup.isoformat() if device.last_backup else None
            }
            for device in devices
        ]
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

def delete_device(device_id):
    try:
        device = Device.query.get(device_id)
        if not device:
            return {"error": "Device não encontrado"}, 404

        db.session.delete(device)
        db.session.commit()

        return {"message": "Device deletado com sucesso"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500