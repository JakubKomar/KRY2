from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.PublicKey import RSA
import hashlib
from Crypto.Random import get_random_bytes


def getRsaKeyFromFile(keyPath):
    return RSA.import_key(open(keyPath).read())
    
def rsaEncWhithKeyFile(message, key):
    cipher = PKCS1_OAEP.new(key)
    
    ciphertext = cipher.encrypt(message)
    return ciphertext

def rsaDecWhithKeyFile(ciphertext, key):
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def easGenKey(bytesNum=16):
    return get_random_bytes(bytesNum)

def easEncWhithKey(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.encrypt(message)
    

def easdecWhithKey(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.decrypt(message)


def md5CreateHash(messege):
    return (hashlib.md5(messege))

def md5CreateHashAndPadding(messege):
    hash=md5CreateHash(messege)
    # to do padding
    return hash

def padding(message,targetLen):
    ...
    