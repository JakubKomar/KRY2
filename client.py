import socket 
import methods as met

def startClient(port,ip = "127.0.0.1" ):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, port))
        print("Successfully connected server.")
        
        clientPubKey=met.getRsaKeyFromFile("cert/clientKeyPub") 
        print("RSA_public_key_sender=\n",clientPubKey.exportKey().decode('utf-8'),"\n",sep="")  
        clientPrivateKey=met.getRsaKeyFromFile("cert/clientKey")
        print("RSA_private_key_sender=\n",clientPrivateKey.exportKey().decode('utf-8'),"\n",sep="")    
        serverPubKey=met.getRsaKeyFromFile("cert/serverKeyPub")      
        print("RSA_public_key_receiver=\n",serverPubKey.exportKey().decode('utf-8'),"\n",sep="") 
        
        while True:
            print("----------------------------------------------------------------")

            inp=input("Enter input:")
            toSend=parseMessage(inp,clientPubKey,clientPrivateKey,serverPubKey)
            for i in range(0,6):
                client.sendall(toSend)
                
                data_tmp = client.recv(1024).decode('utf-8')
                if data_tmp== "ACK-OK":
                    print("The message was successfully delivered")
                    break
                else:
                    print("The message was sent again")
                if(i>4):
                    print("The message cant be delivered")
                    break
            

def parseMessage(message,clientPubKey,clientPrivateKey,serverPubKey):
    relationKey=met.easGenKey()
    print("AES_key=",relationKey.hex())
    
    relationKeyPad=met.rsaPading(relationKey)
    print("AES_key_padding=",relationKeyPad.hex())
    
    inp_b=message.encode('utf-8')
    inp_hex=inp_b.hex()

    md5Hash=met.md5CreateHash(inp_b)
    print("MD5=",md5Hash.hexdigest())

    md5HashPad=met.rsaPading(md5Hash.digest())
    print("MD5_padding=",md5HashPad.hex())
                    
    hashSignature= met.rsaSign(md5HashPad,clientPrivateKey).hex()
    print("RSA_MD5_hash=\n",hashSignature,"\n",sep="")
    
    inp_plus_signature= "{data};{signature}".format(data = inp_hex, signature = hashSignature)
        
    aes_cypherText=met.easEncWhithKey(inp_plus_signature.encode('utf-8'),relationKey).hex()
    print("AES_cipher=\n",aes_cypherText,"\n",sep="")
                                    
                        
    rsa_aes_key= met.rsaEncWhithKeyFile(relationKeyPad,serverPubKey).hex()
    print("RSA_AES_key=\n",rsa_aes_key,"\n",sep="")
            
    cypherText= "{cypherTextPlusSinatureHex};{cypherRelationKey};\004".format(cypherTextPlusSinatureHex = aes_cypherText, cypherRelationKey =rsa_aes_key )
    
    print("Ciphertext=\n",cypherText,"\n",sep="")
    
                
    return cypherText.encode('utf-8')