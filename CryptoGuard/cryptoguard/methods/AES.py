from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from helper.cryption import key_derivation


class AESMethod:
    def encrypt(self, data: bytes, key: str) -> bytes:
        key = key_derivation(key)
        cipher = AES.new(key, AES.MODE_GCM)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        return cipher.nonce + ct_bytes

    def decrypt(self, data: bytes, key: str) -> bytes:
        key = key_derivation(key)
        nonce = data[:16]
        ct = data[16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
