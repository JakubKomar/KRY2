import socket 
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import rsa

def startClient(port):
    HOST = "127.0.0.1"  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, port))
        print("Successfully connected server")
        while True:
            inp=input("Zadej zprávu:")
            toSend=massegeParse(inp)
            client.sendall(toSend)

            #data_tmp = client.recv(1024)
            #print("Server response: ",data_tmp.decode('utf-8'))


def massegeParse(raw):
    res=raw.encode('utf-8')
    rawMd5Hash=hashlib.md5(res)
    print("MD5 hash: ",rawMd5Hash.hexdigest())

    with open('cert/clientKey', mode='rb') as privateKeyFile:
        key_data = privateKeyFile.read()
        public_key = rsa.PrivateKey.load_pkcs1(key_data)
    
    return res


def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key