""" ... """

import rsa

from .settings import SM_KEYS_FILE, SM_KEYS_PATH

FORMAT = 'PEM'


def generate_keys(
    keys_path: str = SM_KEYS_PATH,
    keys_name: str = SM_KEYS_FILE,
    nbits: int = 256
) -> None:
    """ ... """

    public_key, private_key = rsa.newkeys(nbits)

    with open(f'{keys_path}/public_{keys_name}.pem', 'w') as file:
        file.write(public_key.save_pkcs1(FORMAT).decode('utf8'))
    
    with open(f'{keys_path}/private_{keys_name}.pem', 'w') as file:
        file.write(private_key.save_pkcs1(FORMAT).decode('utf8'))