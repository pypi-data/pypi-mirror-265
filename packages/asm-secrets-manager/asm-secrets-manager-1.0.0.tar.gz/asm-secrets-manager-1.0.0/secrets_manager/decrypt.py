""" ... """

import rsa

from base64 import b64decode

from .settings import (
    SM_KEYS_PATH,
    SM_KEYS_FILE,
    SM_SECRETS_PATH,
    SM_SECRETS_FILE_IN,
    SM_SECRETS_FILE_OUT
)


def decrypt(
    text: str,
    keys_path: str = SM_KEYS_PATH,
    keys_name: str = SM_KEYS_FILE,
) -> str:
    """ ... """
    
    with open(f'{keys_path}/private_{keys_name}.pem', 'r') as file:
      base64_decoded = b64decode(text.encode('ASCII'))
      private_key = rsa.PrivateKey.load_pkcs1(file.read().encode('utf8'))
      decrypted_text = rsa.decrypt(base64_decoded, private_key).decode('utf8')

      return decrypted_text


def decrypt_from_file(
    keys_path: str = SM_KEYS_PATH,
    keys_name: str = SM_KEYS_FILE,
    secrets_path: str = SM_SECRETS_PATH,
    secrets_file_input: str = SM_SECRETS_FILE_OUT,
    secrets_file_output: str = SM_SECRETS_FILE_IN
):
   """ ... """

   with open(f'{secrets_path}/{secrets_file_output}', "w") as output_file:
        with open(f'{secrets_path}/{secrets_file_input}', "r") as file:
            for line in file.readlines():
                key_value_pair= line.split('=', 1)
                decrypted_text = decrypt(
                    key_value_pair[1],
                    keys_path=keys_path,
                    keys_name=keys_name
                )
                output_file.write(
                    f"{key_value_pair[0]}={decrypted_text}"
                )