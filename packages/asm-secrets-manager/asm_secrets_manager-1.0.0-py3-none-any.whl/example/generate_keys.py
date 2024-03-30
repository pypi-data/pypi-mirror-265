""" ... """

import argparse

from secrets_manager.generate_keys import generate_keys
from secrets_manager.settings import SM_KEYS_PATH, SM_KEYS_FILE


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
        "--number-bits",
        nargs='?',
        default=256,
        help='Number of bits to generate keys.'
    )
    
    args = parser.parse_args()

    generate_keys(
        keys_path=args.keys_path,
        keys_name=args.keys_name,
        nbits=args.number_bits
    )