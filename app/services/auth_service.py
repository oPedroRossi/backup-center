from ldap3 import Server, Connection, ALL
from app.config import Config


def authenticate_user(username: str, password: str) -> bool:
    user_dn = f"{username}@{Config.AD_DOMAIN}"

    try:
        server = Server(Config.AD_SERVER, get_info=ALL)
        Connection(
            server,
            user=user_dn,
            password=password,
            auto_bind=True
        )
        return True
    except Exception:
        return False
