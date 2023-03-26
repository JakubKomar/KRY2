from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import rsa
def genNewKeys(fileName):
    new_key = RSA.generate(2048)

    private_key = new_key.exportKey("PEM")
    public_key = new_key.publickey().exportKey("PEM")

    fd = open(fileName, "wb")
    fd.write(private_key)
    fd.close()

    fd = open(fileName+"Pub", "wb")
    fd.write(public_key)
    fd.close()

def genRsaSignKeys(fileName):
    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
    fd = open(fileName, "wb")
    fd.write( rsa.PrivateKey.save_pkcs1(privkey))
    fd.close()
    
    fd = open(fileName+"Pub", "wb")
    fd.write( rsa.PublicKey.save_pkcs1(pubkey))
    fd.close()


def genKeysForApk():
    genNewKeys("cert/serverKey")
    genRsaSignKeys("cert/clientKey")

    
if __name__ == "__main__":
    genKeysForApk()