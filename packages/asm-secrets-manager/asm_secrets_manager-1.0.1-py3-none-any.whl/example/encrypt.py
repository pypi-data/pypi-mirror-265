""" ... """

import argparse

from secrets_manager.encrypt import encrypt
from secrets_manager.settings import (
    SM_KEYS_PATH,
    SM_KEYS_FILE
)


if __name__ == "__main__":
    """ ... """
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "text",
        help='Text to encrypt and encode.'
   )
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

    args = parser.parse_args()
    
    base64_encoded = encrypt(
        args.text,
        keys_path=args.keys_path,
        keys_name=args.keys_name
    )

    print(f"The encrypted message is: {base64_encoded}")