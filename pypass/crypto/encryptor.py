"""
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://aws.amazon.com/apache-2-0/

or in the "license" file accompanying this file. This file is distributed on an
"AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""
import logging

import aws_encryption_sdk

from cryptography.fernet import Fernet


logger = logging.getLogger('pypass')


def encrypt_string(key_arn, plaintext, botocore_session=None):

    """Encrypts a string using a KMS customer master key (CMK)

    :param str key_arn: Amazon Resource Name (ARN) of the KMS CMK
    :param bytes plaintext: Data to encrypt
    :param botocore_session: Existing Botocore session instance
    :type botocore_session: botocore.session.Session
    """

    # Create a KMS master key provider
    kms_kwargs = dict(key_ids=[key_arn])
    if botocore_session is not None:
        kms_kwargs['botocore_session'] = botocore_session
    master_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(**kms_kwargs)

    # Encrypt the plaintext source data
    ciphertext, encryptor_header = aws_encryption_sdk.encrypt(
        source=plaintext,
        key_provider=master_key_provider
    )

    # f = Fernet(master_key_provider)
    # ciphertext = f.encrypt(bytes(plaintext, 'utf-8'))

    # print('Ciphertext: ', ciphertext)

    return ciphertext


def decrypt_string(key_arn, ciphertext, botocore_session=None):

    """Decrypts a string using a KMS customer master key (CMK)

    :param str key_arn: Amazon Resource Name (ARN) of the KMS CMK
    :param bytes ciphertext: Data to dencrypt
    :param botocore_session: Existing Botocore session instance
    :type botocore_session: botocore.session.Session
    """

    # Create a KMS master key provider
    kms_kwargs = dict(key_ids=[key_arn])
    if botocore_session is not None:
        kms_kwargs['botocore_session'] = botocore_session
    master_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(**kms_kwargs)

    # Decrypt the ciphertext
    # plaintext, decrypted_header = aws_encryption_sdk.decrypt(
    #     source=ciphertext,
    #     key_provider=master_key_provider
    # )

    f = Fernet(master_key_provider)

    plaintext = f.decrypt(ciphertext)

    print('Decrypted text: ', plaintext)

    return plaintext
