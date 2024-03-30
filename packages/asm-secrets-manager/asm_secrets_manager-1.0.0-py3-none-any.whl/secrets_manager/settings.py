""" ... """

import os


SM_KEYS_PATH = os.environ.get("SM_KEYS_PATH", ".")
SM_KEYS_FILE = os.environ.get("SM_KEYS_FILE", "key")
SM_SECRETS_PATH = os.environ.get("SM_SECRETS_PATH", ".")
SM_SECRETS_FILE_IN = os.environ.get("SM_SECRETS_FILE_IN", ".env")
SM_SECRETS_FILE_OUT = os.environ.get("SM_SECRETS_FILE_OUT", "secrets.txt")