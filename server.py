import socket
import methods as met

def startServer(port):
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    
    serverPubKey=met.getRsaKeyFromFile("cert/serverKeyPub") 
    print("RSA_public_key_sender:\n\n",serverPubKey.exportKey().decode('utf-8'),"\n",sep="")  
    serverPrivateKey=met.getRsaKeyFromFile("cert/serverKey")
    print("RSA_private_key_sender:\n\n",serverPrivateKey.exportKey().decode('utf-8'),"\n",sep="")    
    clientPublicKey=met.getRsaKeyFromFile("cert/clientKeyPub")      
    print("RSA_public_key_receiver:\n\n",clientPublicKey.exportKey().decode('utf-8'),"\n",sep="") 
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Client has joined: {addr}")
                
                buffer=""
                while True:                      
                    data = conn.recv(1024)
                                            
                    buffer+=data.decode('utf-8')
                    if(len(buffer)>0 and buffer[-1]=='\004'):
                        parseBuffer(buffer,serverPubKey,serverPrivateKey,clientPublicKey)
                        buffer=""
                    if not data:
                        print(f"Client disconnected: {addr}")
                        break
                    #conn.sendall(data)

        
def parseBuffer(message,serverPubKey,serverPrivateKey,clientPublicKey):
    pieces=message.split(";")
    print(pieces)
    if len(pieces)<2:
        raise Exception("Chybný formát zprávy")
        
    #zpracovani klice relace
    rsa_aes_key_hex=pieces[1]
    rsa_aes_key=bytearray.fromhex(rsa_aes_key_hex)
    aes_key= met.rsaDecWhithKeyFile(rsa_aes_key,serverPrivateKey)
    print(aes_key.hex()) 
    ########################
    
    aes_cypherText=bytearray.fromhex(pieces[0]) #rozbaleni dat do binarni podoby   
    inp_plus_signature=met.easdecWhithKey(aes_cypherText,aes_key).decode('utf-8')
    print(inp_plus_signature)