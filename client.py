from socket import *
import os 

# Server IP Address and Port
HOST = "18.219.39.168"
PORT = 22
BUFFER_SIZE = 1024

# Setting up our socket
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Connect with server
    print("Trying to connect..")
    clientSocket.connect((HOST, PORT))
    print("Connection established!")

    # Send player name
    playerName = input("Please enter your name: ")
    clientSocket.sendall(playerName.encode())
    
    
except IOError:
    print("File was not found!")
except Exception:
    print("Error!")
    print(Exception + "\n")
finally:
    input("Press Enter to continue") # Here to wait for user input before closing program
    file.close()
    clientSocket.close()