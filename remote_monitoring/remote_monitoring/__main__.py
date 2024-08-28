import argparse

from .utils import key_based_connect


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
