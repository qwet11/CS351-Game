from socket import *

HOST = "localhost"
PORT = 1200

clientSocket = socket(AF_INET, SOCK_STREAM)
print("Trying to connect...")
clientSocket.connect((HOST, PORT))
print("Connection successful!")
print("When you want to exit, please input 'Exit'\n")
while True:
    clientMessage = input("Client message: ")
    if clientMessage == "Exit":
        clientSocket.sendall("Code:20ribjvox".encode())
        break
    clientSocket.sendall(clientMessage.encode())
    serverMessage = clientSocket.recv(1024).decode()
    print("Server message: " + serverMessage)
input("Finished")
clientSocket.close()