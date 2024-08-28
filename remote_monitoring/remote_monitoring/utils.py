from pathlib import Path
from typing import Optional

import paramiko


def key_based_connect(
    host: str, username: str = "qibocal", private_key_password: Optional[str] = None
):
    """
    Setup a connection using ssh.

    Args:
        - host: hostname or ip address for the connection.
        - username: name of the user
        - private_key_password: password used for encrypting the ssh key file.
            Leave it None if the file is not encrypted.
    """
    ssh_key_path = Path.home() / ".ssh" / "id_rsa"
    pkey = paramiko.RSAKey.from_private_key_file(
        ssh_key_path, password=private_key_password
    )
    client = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(policy)
    client.connect(host, username=username, pkey=pkey)
    return client
