# Secrets Manager

Just another python secrets manager library.

This library objective is to aim the variables and secrets management for our software applications on remote repositories on most safe way

## One Way

Also known as hashing, is a cryptographic technique used to transform input data (such as text or files) into a fixed-size string of characters, called a hash value or digest. The key feature of one-way encryption is that it is designed to be irreversible. Once data is hashed, it cannot practically be converted back into its original form.

In relation to the purpose of this library, one-way encryption is discarded because it impedes the maintenance of the remote secrets battery.

## Two ways

Bidirectional encryption allows the recovery of the encrypted secret. Unlike one-way encryption, which produces irreversible hash values, bidirectional encryption allows reversible transformation of data, meaning that encrypted data can be decrypted back to its original form using the same key.

### Symmetric

Refers to the ability to encrypt and decrypt data using the same key in both directions. This means that the same key is used for both encryption and decryption processes, allowing data to be securely transmitted and then decrypted by the intended recipient.

As a consequence of offering maximum security in the use of this library, symmetric encryption is discarded.

### Asymmetric

Involves the use of two different keys for encryption and decryption processes. This form of encryption utilizes a pair of mathematically related keys: a public key and a private key. These keys are asymmetric in the sense that data encrypted with one key can only be decrypted with the other key in the pair.

## Installation

```bash
pip install secrets_manager
```

## Usage

The library has 3 main features and 2 different options for encrypt and decrypt, from terminal or file. Important, non default folders and files should be created and exist.

```bash
mkdir keys
mkdir secrets
```

### Generate keys

Produces a public and private keys to encrypt and decrypt our variable and secrets

```bash
python generate_keys.py
python generate_keys.py --keys-path keys --keys-name example
```

### Encrypt

- Encrypt secret from terminal input.

```bash
python encrypt.py 1234
python encrypt.py 1234 --keys-path keys --keys-name example
```

```bash
The encrypted message is: 1B7oaMagyCMCTNtWV4vE8L2bfKE9Rhv2utLSOkbGdG0=
```

- Encrypt secrets from file.

```bash
python encrypt_file.py
python encrypt_file.py --keys-path keys --keys-name example --secrets-path secrets --secrets-input .env --secrets-output encrypted.txt
```

### Decrypt

- Decrypt secret from terminal input.

```bash
python decrypt.py
python decrypt.py 1B7oaMagyCMCTNtWV4vE8L2bfKE9Rhv2utLSOkbGdG0= --keys-path keys --keys-name example
```

```bash
The decrypted message is: 1234
```

- Decrypt secrets from file.

```bash
python decrypt_file.py
python decrypt_file.py --keys-path keys --keys-name example --secrets-path secrets --secrets-input secrets.txt --secrets-output .env
```

## Configuration

Configuration variables could be overwrite from environment variables or pass params on each method call.

`SM_KEYS_PATH`

Path to save generated keys files. Default `.`.

`SM_KEYS_FILE`

File name for generated keys. Default `key`.

`SM_SECRETS_PATH`

Path to save secrets files for read and write. Default `.`.

`SM_SECRETS_FILE_IN`

File name for secrets to read. Default `.env`.

`SM_SECRETS_FILE_OUT`

File name for secrets to write. Default `secrets.txt`.

## Changelog

Current version is 1.0.0 - see the CHANGELOG file.

## License

This package is licensed under a GPL v.3 style license - see the LICENSE file.
