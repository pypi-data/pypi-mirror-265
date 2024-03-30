""" ... """

import argparse

from secrets_manager.decrypt import decrypt_from_file
from secrets_manager.settings import (
    SM_KEYS_PATH,
    SM_KEYS_FILE,
    SM_SECRETS_FILE_IN,
    SM_SECRETS_FILE_OUT,
    SM_SECRETS_PATH
)


if __name__ == "__main__":
    """ ... """

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--keys-path",
        nargs='?',
        default=SM_KEYS_PATH,
        help='File path for save keys.'
    )
    parser.add_argument(
        "--keys-name",
        nargs='?',
        default=SM_KEYS_FILE,
        help='File name for save keys.'
    )
    parser.add_argument(
        "--secrets-path",
        nargs='?',
        default=SM_SECRETS_PATH,
        help='File path for secrets.'
    )
    parser.add_argument(
        "--secrets-input",
        nargs='?',
        default=SM_SECRETS_FILE_OUT,
        help='File name for read secrets.'
    )
    parser.add_argument(
        "--secrets-output",
        nargs='?',
        default=SM_SECRETS_FILE_IN,
        help='File name for write secrets.'
    )

    args = parser.parse_args()
    

    decrypt_from_file(
        keys_path=args.keys_path,
        keys_name=args.keys_name,
        secrets_path=args.secrets_path,
        secrets_file_input=args.secrets_input,
        secrets_file_output=args.secrets_output
    )