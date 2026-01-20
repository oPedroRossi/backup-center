import os

class Config:
    SECRET_KEY = os.getenv("JWT_SECRET")
    AD_SERVER = os.getenv("AD_URL")
    AD_DOMAIN = os.getenv("AD_DOMAIN")
    AD_BASE_DN = os.getenv("AD_BASEDN")
    AD_USER = os.getenv("AD_USER")
    AD_PASSWORD = os.getenv("AD_PASS")
    ZABBIX_URL = os.getenv("ZABBIX_URL")
    ZABBIX_USER = os.getenv("ZABBIX_USER")
    ZABBIX_PASS = os.getenv("ZABBIX_PASS")
    SERVER_BACKUP_NAME = os.getenv("SERVER_BACKUP_NAME")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")