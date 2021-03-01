from socket import *
import os 

# Server IP Address and Port
HOST = "localhost"
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
    
    # Receive scoreboard
    curr_scoreboard = clientSocket.recv(BUFFER_SIZE).decode()
    print(curr_scoreboard)
    
    while True:
        while True:
            # Receive current board 
            curr_board = clientSocket.recv(BUFFER_SIZE).decode()
            print(curr_board)
            
            # Check if this is the player's move (1 for yes, 0 for no)
            turn_checker = clientSocket.recv(BUFFER_SIZE).decode()
            
            if (turn_checker == "0"):
                # Wait for other player
                print("Waiting for other player's move...")
            elif (turn_checker == "1"):
                while True:
                    try: 
                        # Get player move 
                        player_move = input("Your turn! Which box : ")
                        # Checks if player_move is a number
                        if (int(player_move) < 1 or int(player_move) > 9):
                            print("Wrong Input! Try again")
                        else:
                            clientSocket.sendall(player_move.encode())
                            # Check if box is not occupied
                            fill_checker = clientSocket.recv(BUFFER_SIZE).decode()
                            if (fill_checker == "1"):
                                # Box is occupied. Try again
                                print("Place already filled. Try again!!")
                                continue
                            elif (fill_checker == "0"): 
                                # Everything in order
                                break
                            else: 
                                # Should never run. DEBUGGING
                                input("ERROR 2. Please Exit")
                    except(ValueError):
                        print("Please input a number (1-9)")
                        continue
            else:
                # Should never run. DEBUGGING
                input("ERROR 1. Please Exit")
                
            # Check if we should continue
            continue_checker = clientSocket.recv(BUFFER_SIZE).decode()
            
            if (continue_checker == "Continue"):
                continue
            elif (continue_checker == "Finish"):
                curr_board = clientSocket.recv(BUFFER_SIZE).decode()
                print(curr_board)
                game_message = clientSocket.recv(BUFFER_SIZE).decode()
                print(game_message)
                break
        
        # Receive scoreboard
        curr_scoreboard = clientSocket.recv(BUFFER_SIZE).decode()
        print(curr_scoreboard)
    
        
    
except Exception:
    print("Error!")
    print(str(Exception) + "\n")
finally:
    input("Press Enter to continue") # Here to wait for user input before closing program
    clientSocket.close()