from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
import Crypto.Hash.MD5 as MD5

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

def rsaCreateSignature(hashObject, key):
    cipher = pkcs1_15.new(key)
    return cipher.sign(hash)

def rsaVerifySignature(hashObject,signature, key):
    try:
        pkcs1_15.new(key).verify(hashObject, signature)
        return True
    except (ValueError, TypeError):
        return False

def easGenKey(bytesNum=16):
    return get_random_bytes(bytesNum)

def easEncWhithKey(message, key):
    cipher = AES.new(key, AES.MODE_CFB)
    cipher_text = cipher.encrypt(message)
    iv = cipher.iv
    return iv+cipher_text
    


def easdecWhithKey(message, key):
    cipher = AES.new(key, AES.MODE_CFB)
    if(len(message)<16):
        raise Exception("aes decription error: len of message is to low")
    
    iv=message[0:AES.block_size]
    cipher_text=message[AES.block_size:]

    decrypt_cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    return decrypt_cipher.decrypt(cipher_text)


def md5CreateHash(messege):
    return MD5.new(messege)

def md5CreateHashAndPadding(messege):
    hash=md5CreateHash(messege)
    # to do padding
    return hash

def padding(message,targetLen):
    ...
    