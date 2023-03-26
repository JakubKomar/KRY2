from Crypto.PublicKey import RSA

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

def genKeysForApk():
    genNewKeys("cert/serverKey")
    genNewKeys("cert/clientKey")

    
if __name__ == "__main__":
    genKeysForApk()