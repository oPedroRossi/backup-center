import requests
from app.config import Config
from app.utils.metrics import bytes_to_gb, status_by_percent, status_cpu

def zabbix_login():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": Config.ZABBIX_USER,
            "password": Config.ZABBIX_PASS
        },
        "id": 1
    }
    r = requests.post(Config.ZABBIX_URL, json=payload)
    return r.json()["result"]


def get_host_id(token, host_name):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "search": {
                "name": host_name
            }
        },
        "auth": token,
        "id": 2
    }

    r = requests.post(Config.ZABBIX_URL, json=payload)
    result = r.json()["result"]

    if not result:
        raise Exception("Host não encontrado no Zabbix")

    return result[0]["hostid"]

def parse_metrics(items):
    cpu_load = None

    mem_total = mem_free = None
    disk_total = disk_free = disk_used = None

    for item in items:
        key = item.get("key_")
        raw_value = item.get("lastvalue")

        try:
            value = float(raw_value)
        except (ValueError, TypeError):
            continue

        # CPU
        if key == "system.cpu.load[percpu,avg1]":
            cpu_load = value

        # MEMÓRIA
        elif key == "vm.memory.size[total]":
            mem_total = value

        elif key == "vm.memory.size[free]":
            mem_free = value

        # DISCO C:
        elif key == "vfs.fs.size[C:,total]":
            disk_total = value

        elif key == "vfs.fs.size[C:,free]":
            disk_free = value

        elif key == "vfs.fs.size[C:,used]":
            disk_used = value

    # MEMÓRIA
    mem_used = mem_total - mem_free if mem_total and mem_free else None
    mem_percent = (mem_used / mem_total * 100) if mem_used and mem_total else None

    # DISCO
    disk_percent = (disk_used / disk_total * 100) if disk_used and disk_total else None

    return {
        "cpu": {
            "load": round(cpu_load, 2) if cpu_load else None,
            "status": status_cpu(cpu_load) if cpu_load else "unknown"
        },
        "memory": {
            "total_gb": bytes_to_gb(mem_total) if mem_total else None,
            "used_gb": bytes_to_gb(mem_used) if mem_used else None,
            "free_gb": bytes_to_gb(mem_free) if mem_free else None,
            "percent": round(mem_percent, 1) if mem_percent else None,
            "status": status_by_percent(mem_percent) if mem_percent else "unknown"
        },
        "disk": {
            "total_gb": bytes_to_gb(disk_total) if disk_total else None,
            "used_gb": bytes_to_gb(disk_used) if disk_used else None,
            "free_gb": bytes_to_gb(disk_free) if disk_free else None,
            "percent": round(disk_percent, 1) if disk_percent else None,
            "status": status_by_percent(disk_percent) if disk_percent else "unknown"
        }
    }


def get_server_metrics():
    token = zabbix_login()
    hostid = get_host_id(token, Config.SERVER_BACKUP_NAME)

    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "hostids": hostid,
            "output": ["key_", "name", "lastvalue"]
        },
        "auth": token,
        "id": 3
    }

    r = requests.post(Config.ZABBIX_URL, json=payload)
    items = r.json()["result"]

    metrics = parse_metrics(items)
    return metrics

