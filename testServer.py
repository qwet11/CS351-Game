from socket import *

HOST = "localhost"
PORT = 1200

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",PORT))
serverSocket.listen(1)

print("Waiting for connection...")
while True:
    try: 
        connectionSocket, address = serverSocket.accept()
        print("Connection successful!")
        while True:
            clientMessage = connectionSocket.recv(1024).decode()
            if clientMessage == "Code:20ribjvox":
                print("Client disconnected")
                connectionSocket.close()
                break
            else: 
                print("Client message: " + clientMessage)
                serverMessage = input("Server message: ")
                connectionSocket.sendall(serverMessage.encode())
    except Exception: 
        print(Exception)
    else:
        print("\n Cycle successful \n")