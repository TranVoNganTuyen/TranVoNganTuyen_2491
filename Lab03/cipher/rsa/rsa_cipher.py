import rsa
import os

class RSACipher:
    def __init__(self):
        self.public_key_file = "cipher/rsa/keys/public.pem"
        self.private_key_file = "cipher/rsa/keys/private.pem"

    def generate_keys(self):
        public_key, private_key = rsa.newkeys(512)

        os.makedirs("cipher/rsa/keys", exist_ok=True)

        with open(self.public_key_file, "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        with open(self.private_key_file, "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

    def load_keys(self):
        with open(self.private_key_file, "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        with open(self.public_key_file, "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        return private_key, public_key

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode(), key)

    def decrypt(self, ciphertext, key):
        return rsa.decrypt(ciphertext, key).decode()

    def sign(self, message, private_key):
        return rsa.sign(message.encode(), private_key, "SHA-256")

    def verify(self, message, signature, public_key):
        try:
            rsa.verify(message.encode(), signature, public_key)
            return True
        except:
            return False