
import hashlib

# object encode / decode

class ObjectCodec():

    @staticmethod
    def encode(arg_object):
        return arg_object.encode('utf-8')

    @staticmethod
    def decode(arg_object):
        return arg_object.decode('utf-8')

# hashing

class Hashing():

    @staticmethod
    def hash_sha1(arg_object):
        return hashlib.sha1(arg_object).hexdigest()

    @staticmethod
    def integer_hash(arg_hex_digest):
        return int(arg_hex_digest[:8], 16) # 8 hex digits of precision

# END ##########################################################################
