from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5
from Crypto.Util.number import bytes_to_long,long_to_bytes

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

def rsaSign(text,privateKey):
    if len(text)>256:
        raise Exception("blbě")
    D=  bytes_to_long(text)
    S=pow(D,privateKey.d, privateKey.n)

    return long_to_bytes(S)

def rsaPading(text,target=214):
    toBePad=target-len(text)
    pading=get_random_bytes(toBePad)
    res=text+pading
    return res

def rsaUnPading(text,textLen):
    return text[:textLen]

def rsaSignVer(text,publicKey):
    S=  bytes_to_long(text)
    res=pow(S,publicKey.e ,publicKey.n)
    return long_to_bytes(res)

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
    