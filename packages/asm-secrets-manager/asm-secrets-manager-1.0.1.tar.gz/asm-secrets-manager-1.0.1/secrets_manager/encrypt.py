""" ... """

import rsa

from base64 import b64encode

from .settings import (
    SM_KEYS_PATH,
    SM_KEYS_FILE,
    SM_SECRETS_PATH,
    SM_SECRETS_FILE_IN,
    SM_SECRETS_FILE_OUT
)


def encrypt(
    text: str,
    keys_path: str = SM_KEYS_PATH,
    keys_name: str = SM_KEYS_FILE,
) -> str:
    """ ... """
    
    with open(f'{keys_path}/public_{keys_name}.pem', 'r') as file:
      public_key = rsa.PublicKey.load_pkcs1(file.read().encode('utf8'))
      encrypted_tex = rsa.encrypt(text.encode('utf8'), public_key)
      base64_encoded = b64encode(encrypted_tex).decode('ASCII')
      
    return base64_encoded


def encrypt_from_file(
    keys_path: str = SM_KEYS_PATH,
    keys_name: str = SM_KEYS_FILE,
    secrets_path: str = SM_SECRETS_PATH,
    secrets_file_input: str = SM_SECRETS_FILE_IN,
    secrets_file_output: str = SM_SECRETS_FILE_OUT
):
    """ ... """
    
    with open(f'{secrets_path}/{secrets_file_output}', "w") as output_file:
        with open(f'{secrets_path}/{secrets_file_input}', "r") as file:
            for line in file.readlines():
                key_value_pair= line.split('=', 1)
                base64_encoded = encrypt(
                    key_value_pair[1],
                    keys_path=keys_path,
                    keys_name=keys_name
                )
                output_file.write(f"{key_value_pair[0]}={base64_encoded}\n")