import socket


def startServer(port):
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Client has joined: {addr}")
                    while True:
                        data = conn.recv(1024)
                        print(data.decode('utf-8'))
                        if not data:
                            break
                        #conn.sendall(data)
    except Exception as ex:
        print("Error:",ex)