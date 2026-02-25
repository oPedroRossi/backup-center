import paramiko


def get_config_linux(device):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=device.ip_address,
        username=device.username,
        password=device.password
    )

    stdin, stdout, stderr = ssh.exec_command("cat /etc/asterisk/sip.conf")

    output = stdout.read().decode()
    ssh.close()

    return output
