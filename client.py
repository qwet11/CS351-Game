from socket import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from threading import Thread

# Server IP Address and Port
HOST = "localhost"
PORT = 65000
BUFFER_SIZE = 1024

# Setting up our socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# CREATE TWO SOCKETS
# ONE FOR THE GAME AND FOR THE CHAT

# GLOBALS
player_move = "holdondude"

class Board(QMainWindow):
    def __init__(self):
        #super().__init__()
        QThread.__init__(self)
        uic.loadUi('Board.ui', self)
        self.setWindowTitle('Board Game')
        self.send_move_bt.clicked.connect(self.sendMove)
        self.error_lbl.setText("")
        self.turn_lbl.setText("")
        
    def sendMove(self):
        global player_move
        player_move = board.input_edit.text()
        self.input_edit.setText("")
        self.error_lbl.setText("")

def BoardGame():
    global board, player_move
    #Starting Game
    while True:
        # Playing Game
        while True:
            # Receive current board 
            curr_board = clientSocket.recv(BUFFER_SIZE).decode()
            
            # Change GUI board to current board
            board.board_lbl.setText(curr_board)
            print(curr_board)
            clientSocket.sendall("Received".encode())            
            
            # Check if this is the player's move (1 for yes, 0 for no)
            turn_checker = clientSocket.recv(BUFFER_SIZE).decode()
            print("check: " + str(turn_checker) + "\n") #Debugging only
            clientSocket.sendall("Received".encode())
            
            if (turn_checker == "0"):
                # Hide button and input box
                board.send_move_bt.hide() 
                board.input_edit.hide()
                
                # Wait for other player 
                board.turn_lbl.setText("Waiting for other player's move...")
                print("Waiting for other player's move...")
            elif (turn_checker == "1"):
                # Show button and input box
                board.send_move_bt.show()
                board.input_edit.show()
                
                while True:
                    try: 
                        # Inform player of his turn
                        board.turn_lbl.setText("Your Turn!")
                        print("Your Turn!")
                        
                        # Wait for player's input
                        player_move = "holdondude"
                        while (player_move == "holdondude"): { }
                        
                        # Checks if player_move is a number
                        if (int(player_move) < 1 or int(player_move) > 9):
                            board.error_lbl.setText("Please input a number (1-9)")
                            print("Please input a number (1-9)")
                        else:
                            clientSocket.sendall(player_move.encode())
                            # Check if box is not occupied
                            fill_checker = clientSocket.recv(BUFFER_SIZE).decode()
                            clientSocket.sendall("Received".encode())
                            if (fill_checker == "1"):
                                # Box is occupied. Try again
                                board.error_lbl.setText("Place already filled. Try again!!")
                                print("Place already filled. Try again!!")
                                continue
                            elif (fill_checker == "0"): 
                                # Everything in order
                                player_move = "holdondude"
                                break
                            else: 
                                # Should never run. DEBUGGING
                                input("ERROR 2. Please Exit")
                    except(ValueError):
                        board.error_lbl.setText("Please input a number (1-9)")
                        print("Please input a number (1-9)")
                        continue
            else:
                # Should never run. DEBUGGING
                input("ERROR 1. Please Exit")
                
            # Check if we should continue
            continue_checker = clientSocket.recv(BUFFER_SIZE).decode()
            clientSocket.sendall("Received".encode())
            
            if (continue_checker == "Continue"):
                continue
            elif (continue_checker == "Finish"):
                # Update board
                curr_board = clientSocket.recv(BUFFER_SIZE).decode()
                clientSocket.sendall("Received".encode())
                print(curr_board)
                
                game_message = clientSocket.recv(BUFFER_SIZE).decode()
                clientSocket.sendall("Received".encode())
                
                # Show game message
                board.error_lbl.setText(game_message)
                print(game_message)
                
                # Reset turn label
                board.turn_lbl.setText("")
                break
            else:
                # Should never run. DEBUGGING
                input("ERROR 3. Please Exit")
            

        """
        # Receive scoreboard
        curr_scoreboard = clientSocket.recv(BUFFER_SIZE).decode()
        print(curr_scoreboard)
        """

try:
    # Connect with server
    print("Trying to connect..")
    clientSocket.connect((HOST, PORT))
    print("Connection established!")

    # Send player name
    playerName = input("Please enter your name: ")
    clientSocket.sendall(playerName.encode())
    print("Waiting for other player to connect...")
    
    """
    # Receive scoreboard
    curr_scoreboard = clientSocket.recv(BUFFER_SIZE).decode()
    print(curr_scoreboard)
    """
    
    app = QApplication(sys.argv)
    board = Board()
    board.show()

    
    game_thread = Thread(target=BoardGame)
    game_thread.start()
    
    app.exec_()
    #sys.exit(app.exec_())        
    
except Exception as e:
    print("Error!")
    print(str(e) + "\n")
finally:
    input("Press Enter to continue") # Here to wait for user input before closing program
    clientSocket.close()
   
