from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

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
    DB_host = os.getenv("DB_HOST")
    DB_port = DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_user = os.getenv("DB_USER")
    DB_password = quote_plus(os.getenv("DB_password"))
    DB_name = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_user}:{DB_password}@{DB_host}:{DB_port}/{DB_name}"
    HUAWEI_user = os.getenv("huawei_user")
    HUAWEI_pass = os.getenv("huawei_pass")
    SOPHOS_user = os.getenv("sophos_user")
    SOPHOS_pass = os.getenv("sophos_pass")
    FORTINET_user = os.getenv("fortinet_user")
    FORTINET_pass = os.getenv("fortinet_pass")
    HPE_user = os.getenv("hpe_user")
    HPE_pass = os.getenv("hpe_pass")