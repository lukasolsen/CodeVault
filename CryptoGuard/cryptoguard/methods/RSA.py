import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class RSAMethod:
    def __init__(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def generate_key_pair(self) -> None:
        # Check if keys already exist
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            print("RSA key pair already exists.")
            return

        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize keys to PEM format
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Write keys to files
        with open(self.private_key_path, 'wb') as private_key_file:
            private_key_file.write(private_key_pem)

        with open(self.public_key_path, 'wb') as public_key_file:
            public_key_file.write(public_key_pem)

        print(
            f"RSA key pair generated and saved to {self.private_key_path} and {self.public_key_path}.")

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        self.generate_key_pair()
        # Load public key
        with open(self.public_key_path, 'rb') as public_key_file:
            public_key_pem = public_key_file.read()
            public_key = serialization.load_pem_public_key(
                public_key_pem, backend=default_backend()
            )

        # Encrypt the data
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        self.generate_key_pair()
        # Load private key
        with open(self.private_key_path, 'rb') as private_key_file:
            private_key_pem = private_key_file.read()
            private_key = serialization.load_pem_private_key(
                private_key_pem, password=None, backend=default_backend()
            )

        # Decrypt the data
        data = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return data
