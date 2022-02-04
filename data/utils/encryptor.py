import hashlib
from decouple import config

class Encryptor:
    @staticmethod
    def md5_encryption(raw_value):
        return hashlib.md5(raw_value.encode(config("ENCODING"))).hexdigest()
