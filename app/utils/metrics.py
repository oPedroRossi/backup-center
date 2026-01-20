def bytes_to_gb(value):
    return round(value / 1024 / 1024 / 1024, 2)


def status_by_percent(percent):
    if percent < 70:
        return "ok"
    elif percent < 85:
        return "warning"
    return "critical"


def status_cpu(load):
    if load < 0.7:
        return "ok"
    elif load < 1.0:
        return "warning"
    return "critical"
