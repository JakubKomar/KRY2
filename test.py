
import methods as met
from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
import Crypto.Hash.MD5 as MD5
import rsa
text="hello wodwdwadwadrd"
text2="hello word"

with open('cert/clientKey', mode='rb') as privatefile:
    keydata = privatefile.read()
privatKey = rsa.PrivateKey.load_pkcs1(keydata)

with open('cert/clientKeyPub', mode='rb') as privatefile:
    keydata = privatefile.read()
publicKey = rsa.PublicKey.load_pkcs1(keydata)

#print("RSA_private_key_sender:\n\n",serverPrivateKey.exportKey().decode('utf-8'),"\n",sep="")    

inp_b=text.encode('utf-8')

hash = MD5.new(inp_b).digest()

hash2=hash
for  i in range (0,5):
    hash2+=hash2

print(len(hash2))
crypto = rsa.decrypt(hash2[0:245],privatKey)
print(len(crypto))
plain=rsa.encrypt(crypto, publicKey)
