import argparse
from pathlib import Path

import paramiko


def key_based_connect(host: str, username="qibocal", private_key_password=None):
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


def main():
    """ssh connection"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--username", type=str, default="qibocal")
    parser.add_argument("--private_key_password", type=str, default=None)
    args = parser.parse_args()
    client = key_based_connect(
        args.host, args.username, private_key_password=args.private_key_password
    )


if __name__ == "__main__":
    main()
