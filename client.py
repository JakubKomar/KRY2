import socket 


def startClient(port):
    print("client")
    HOST = "127.0.0.1"  # The server's hostname or IP address

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, port))

    client.send("I am CLIENT\n")
    from_server = client.recv(4096)
    print("I received from SERVER %s" %from_server)
    print("Send your character to SERVER")
    input1=str(input())
    client.send(input1)

    client.close()