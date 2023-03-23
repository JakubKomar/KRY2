import socket 
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import methods as met

def startClient(port):
    HOST = "127.0.0.1"  # The server's hostname or IP address

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, port))
        print("Uspesne pripojen k serveru.")
        
        clientPubKey=met.getRsaKeyFromFile("cert/clientKeyPub") 
        print("RSA_verejny_klic_odesilatele:\n\n",clientPubKey.exportKey().decode('utf-8'),"\n",sep="")  
        clientPrivateKey=met.getRsaKeyFromFile("cert/clientKey")
        print("RSA_privatni_klic_odesilatele:\n\n",clientPrivateKey.exportKey().decode('utf-8'),"\n",sep="")    
        serverPubKey=met.getRsaKeyFromFile("cert/serverKeyPub")      
        print("RSA_verejny_klic_prijemce:\n\n",serverPubKey.exportKey().decode('utf-8'),"\n",sep="") 
        
        while True:
            inp=input("Zadej vstup:")
            
            relationKey=met.easGenKey()
            print("AES_key:",relationKey.hex())
            
            # todo AES_key pading 
            
            inp_b=inp.encode('utf-8')
            inp_hex=inp_b.hex()

            md5Hash=met.md5CreateHash(inp_b)
            print("MD5Hash:",md5Hash.hexdigest())

            # todo MD5_padding 
                            
            hashSignature= met.rsaEncWhithKeyFile(md5Hash.digest(),clientPrivateKey).hex()
            print("RSA hash signature:\n",hashSignature,"\n",sep="")
            
            inp_plus_signature= "{data};{signature}".format(data = inp_hex, signature = hashSignature)
            print("Bruh:\n",inp_plus_signature.encode('utf-8'),"\n",sep="")
            
            aes_cypherText=met.easEncWhithKey(inp_plus_signature.encode('utf-8'),relationKey).hex()
            print("AES_cipher:\n",aes_cypherText,"\n",sep="")
                                         
                             
            rsa_aes_key= met.rsaEncWhithKeyFile(relationKey,serverPubKey).hex()
            print("RSA_AES_key:\n",rsa_aes_key,"\n",sep="")
                  
            cypherText= "{cypherTextPlusSinatureHex};{cypherRelationKey};\004".format(cypherTextPlusSinatureHex = aes_cypherText, cypherRelationKey =rsa_aes_key )
            
            print("Zasifrovany text:\n",cypherText,"\n",sep="")
            
                       
            toSend=cypherText.encode('utf-8')
            client.sendall(toSend)
            print("Zpráva odeslána")
            #data_tmp = client.recv(1024)
            #print("Server response: ",data_tmp.decode('utf-8'))

