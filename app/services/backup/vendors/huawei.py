import paramiko
import time


def get_config(device):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=device.ip_address,
        username=device.username,
        password=device.password,
        timeout=15
    )

    shell = ssh.invoke_shell()
    shell.send("screen-length 0 temporary\n")
    shell.send("display current-configuration\n")

    time.sleep(5)

    output = shell.recv(999999).decode()
    ssh.close()

    return output
