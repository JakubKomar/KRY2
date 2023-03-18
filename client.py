import socket 


def startClient(port):
    print("client")
    HOST = "127.0.0.1"  # The server's hostname or IP address

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, port))

    toSend=input("Zadej zprávu:")
    client.sendall(toSend.encode('utf-8'))

    data_tmp = client.recv(1024)
    print("Server response: ",data_tmp.decode('utf-8'))
    client.close()