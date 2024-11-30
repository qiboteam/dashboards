from pathlib import Path
from typing import Optional

import paramiko
import scp


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


def copy_back_remote_report(
    ssh_client: paramiko.SSHClient,
    platform: str,
    report_directory_name: str,
    remote_monitoring_path: str,
    local_directory_path: Path,
) -> Path:
    """Copy the qibocal output locally in the container."""
    remote_report_path = f"{remote_monitoring_path}/{platform}/{report_directory_name}"
    local_report_path = local_directory_path / platform / report_directory_name
    local_report_path.mkdir(parents=True)
    scp_client = scp.SCPClient(ssh_client.get_transport())
    scp_client.get(remote_report_path, str(local_report_path.parent), recursive=True)
    return local_report_path
