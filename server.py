import socket
import methods as met

def startServer(port, ip = "127.0.0.1"):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print("Server ready...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Client has joined: {addr}")
                serverPubKey=met.getRsaKeyFromFile("cert/serverKeyPub") 
                
                print("RSA_public_key_sender=\n",serverPubKey.exportKey().decode('utf-8'),"\n",sep="")  
                serverPrivateKey=met.getRsaKeyFromFile("cert/serverKey")
                print("RSA_private_key_sender=\n",serverPrivateKey.exportKey().decode('utf-8'),"\n",sep="")    

                clientPublicKey=met.getRsaKeyFromFile("cert/clientKeyPub")      
                print("RSA_public_key_receiver=\n",clientPublicKey.exportKey().decode('utf-8'),"\n",sep="") 
                   
                buffer=""
                while True:                   
                    data = conn.recv(1024)                                         
                    buffer+=data.decode('utf-8')
                    if(len(buffer)>0 and buffer[-1]=='\004'):
                        print("----------------------------------------------------------------") 
                        var=parseBuffer(buffer,serverPubKey,serverPrivateKey,clientPublicKey)
                        buffer=""
                        if var:
                            conn.sendall(("ACK-OK").encode("utf-8"))
                        else:
                            conn.sendall(("ACK-NOK").encode("utf-8"))
                    if not data:
                        print(f"Client disconnected: {addr}")
                        break
                    #conn.sendall(data)

        
def parseBuffer(message,serverPubKey,serverPrivateKey,clientPublicKey):
    print("Ciphertext=\n",message,"\n",sep="")
    
    pieces=message.split(";")
    if len(pieces)<2:
        raise Exception("Chybný formát zprávy")
        
    #zpracovani klice relace
    rsa_aes_key_hex=pieces[1]
    print("RSA_AES_key=\n",rsa_aes_key_hex,"\n",sep="")
    rsa_aes_key=bytearray.fromhex(rsa_aes_key_hex)
    
    aes_cypherText=bytearray.fromhex(pieces[0]) #rozbaleni dat do binarni podoby  
    print("AES_cipher=\n",pieces[0],"\n",sep="")
    
    aes_key= met.rsaUnPading(met.rsaDecWhithKeyFile(rsa_aes_key,serverPrivateKey),16)
    print("AES_key=",aes_key.hex())


    inp_plus_signature=(met.easdecWhithKey(aes_cypherText,aes_key)).decode('utf-8')
    print("Text_hash=\n",inp_plus_signature, "\n",sep="" )
    
    
    pieces2=inp_plus_signature.split(";")
    if len(pieces2)<2:
        raise Exception("Chybný formát zprávy")
    
    plainText_b=bytearray.fromhex(pieces2[0])
    
    # plainText_b[2]=ord('4') # simulating ilegal modification of message
    
    plainText=plainText_b.decode('utf-8')
    print("Plaintext=",plainText, "\n",sep="" )
    
    
    hashSignatureRsa=bytearray.fromhex(pieces2[1])
    md5=met.rsaUnPading(met.rsaSignVer(hashSignatureRsa,clientPublicKey),16)
    print("MD5=",md5.hex() )
        
    md5HashCalc=met.md5CreateHash(plainText_b).digest()
    if md5HashCalc==md5:
        print("The integrity of the message has not been compromised.")
        return True
    else:
        print("The integrity of the message has been compromised.")
        return False
    