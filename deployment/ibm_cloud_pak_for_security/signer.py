# coding: utf-8
import base64
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography import x509
import hashlib
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import X509Store, X509StoreContext, FILETYPE_PEM
import os
import shutil


class Encryptor(object):
    KEY_FILE_PATH = None
    KEY = None
    PASSWORD = None
    MESSAGES = []

    def __init__(self, filepaths, cert=None, password=None):
        if isinstance(filepaths, list) and len(filepaths) > 0 and cert:
            self.KEY = cert
            if len(filepaths) > 0:
                try:
                    result = self.validate_chain(filepaths, cert)
                    if not result:
                        print('verify:error:untrusted certificate')
                        exit(6)
                except Exception as ex:
                    print('verify:error:certificate signature failure: ' + str(ex))
                    exit(5)
                self.MESSAGES.append('cert chain validated')
        else:
            if cert:
                self.KEY = cert
            elif filepaths:
                self.KEY_FILE_PATH = filepaths
        self.PASSWORD = password

    def validate_chain(self, file_names, last_cert):
        store = X509Store()
        for cert_file in file_names:
            with open(cert_file, 'rb') as f:
                cert = load_certificate(FILETYPE_PEM, f.read())
                store.add_cert(cert)
        store_ctx = X509StoreContext(store, load_certificate(FILETYPE_PEM, last_cert))
        result = store_ctx.verify_certificate()
        if result is None:
            return True
        else:
            return False

    def encrypt(self, message):
        private_key = self._get_private_key()
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def is_certificate(self, file_path_or_content):
        if isinstance(file_path_or_content, list):
            file_path_or_content = file_path_or_content[0]
        if isinstance(file_path_or_content, bytes):
            return 'CERTIFICATE' in file_path_or_content.decode('utf-8')
        with open(file_path_or_content, "rb") as f:
            for l in f.readlines():
                if 'CERTIFICATE' in l.decode('utf-8'):
                    return True
        return False

    def verify(self, message, signature):
        if self.is_certificate(self.KEY_FILE_PATH or self.KEY):
            public_key = self._get_public_key_from_cert()
        else:
            public_key = self._get_public_key()

        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def _get_public_key(self):

        if self.KEY_FILE_PATH:
            with open(self.KEY_FILE_PATH, "rb") as key_file:
                data = key_file.read()
        elif self.KEY:
            data = self.KEY

        public_key = serialization.load_pem_public_key(
                    data, backend=default_backend()
                )
        return public_key

    def _get_public_key_from_cert(self):
        if self.KEY_FILE_PATH:
            with open(self.KEY_FILE_PATH, "rb") as key_file:
                data = key_file.read()
        elif self.KEY:
            data = self.KEY
        cert = x509.load_pem_x509_certificate(data, default_backend())
        public_key = cert.public_key()
        return public_key

    def _get_private_key(self):
        with open(self.KEY_FILE_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=self.PASSWORD,
                backend=default_backend()
            )
        return private_key


if __name__ == "__main__":
    signature_path_hashes = 'meta/hashes.dat'
    signature_path_check = 'meta/check.dat'
    signature_path_cert = 'meta/cert.pem'

    package_file = sys.argv[-1]

    bundle_files = []
    for r, d, f in os.walk(package_file):
        for file in f:
            bundle_files.append(os.path.join(r, file)[len(package_file)+1:])
    if sys.argv[1] == 'sign':
        encryptor = Encryptor(sys.argv[2])
        hash_lines = ''
        if signature_path_hashes not in bundle_files:
            os.mkdir(os.path.join(package_file, 'meta'))
            for f in bundle_files:
                with open(os.path.join(package_file, f), 'rb') as file:
                    content = file.read()
                content_hash = hashlib.sha256(content).hexdigest()
                hash_lines += f + ' ' + content_hash + '\n'
            with open(os.path.join(package_file, signature_path_hashes), 'w') as file:
                file.write(hash_lines)
            check = encryptor.encrypt(hash_lines.encode())
            check = base64.b64encode(check)
            with open(os.path.join(package_file, signature_path_hashes), 'w') as file:
                file.write(hash_lines)
            with open(os.path.join(package_file, signature_path_check), 'w') as file:
                file.write(check.decode('utf-8'))
            shutil.copyfile(sys.argv[3], os.path.join(package_file, signature_path_cert))
            print('sign:ok')
        else:
            print('sign:error:file has been signed already')
            exit(1)
    elif sys.argv[1] == 'verify':
        with open(os.path.join(package_file, signature_path_cert), 'rb') as file:
            cert = file.read()
        encryptor = Encryptor(sys.argv[2:-1], cert=cert)
        if signature_path_check in bundle_files and signature_path_hashes in bundle_files:
            with open(os.path.join(package_file, signature_path_hashes), 'r') as file:
                hash_content = file.read()
            hash_lines = hash_content.splitlines()
            with open(os.path.join(package_file, signature_path_check), 'r') as file:
                check_content = base64.b64decode(file.read())
            try:
                encryptor.verify(hash_content.encode(), check_content)
            except InvalidSignature as ex:
                print('verify:error:hashes signature incorrect:'+str(ex))
                exit(3)
            for hash_item in hash_lines:
                hash_items = hash_item.split()
                bundle_file_path = hash_items[0]
                with open(os.path.join(package_file, bundle_file_path), 'rb') as file:
                    content = file.read()
                bundle_file_sign = hashlib.sha256(content).hexdigest()
                if bundle_file_sign == hash_items[1]:
                    bundle_files.remove(bundle_file_path)
            bundle_files.remove(signature_path_hashes)
            bundle_files.remove(signature_path_check)
            bundle_files.remove(signature_path_cert)
            if bundle_files:
                print('verify:error:signature mismatch: ' + str(bundle_files))
                exit(4)
            else:
                message = 'verify:ok'
                for m in encryptor.MESSAGES:
                    message += ':' + m
                print(message)
        else:
            print('verify:error:archive is not signed')
            exit(2)

