from socket import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import time
from threading import Thread

# Server IP Address and Port
HOST = "ec2-3-142-208-64.us-east-2.compute.amazonaws.com"
PORT1 = 64000
PORT2 = 65000
BUFFER_SIZE = 1024

# Setting up our socket
clientGameSocket = socket(AF_INET, SOCK_STREAM)
clientChatSocket = socket(AF_INET, SOCK_STREAM)

# GLOBALS
player_move = "holdondude"
playerName = "f34h9fvh394vn9fu493oihtnb93yw9yfu9nh49"


# Game Functions
class Board(QMainWindow):
    def __init__(self):
        QThread.__init__(self)
        uic.loadUi('Board.ui', self)
        self.setWindowTitle('Tic-Tac-Toe Game')
        self.send_move_bt.hide()
        self.input_edit.hide()
        self.send_move_bt.clicked.connect(self.sendMove)
        self.send_chat_bt.clicked.connect(self.sendChat)
        self.error_lbl.setText("")
        self.turn_lbl.setText("")
        self.scoreboard_lbl.setText("")
        self.chat_output_box.setText("Please enter your name!")
        self.chat_output_box.append("Max characters used for the name is 11!")
        
    def sendMove(self):
        global player_move, clientChatSocket
        player_move = self.input_edit.text()
        self.input_edit.setText("")
        self.error_lbl.setText("")
        
    def sendChat(self):
        global playerName
        
        if (playerName == "f34h9fvh394vn9fu493oihtnb93yw9yfu9nh49" and self.chat_input_box.text() != ""):
            playerName = self.chat_input_box.text()
            self.chat_output_box.clear() 
        elif (self.chat_input_box.text() != ""):
            clientChatSocket.sendall(self.chat_input_box.text().encode())
             
        self.chat_input_box.clear()

def UpdateBoard(curr_board):
    global board
    board.box1.setText(curr_board[0])
    board.box2.setText(curr_board[1])
    board.box3.setText(curr_board[2])
    board.box4.setText(curr_board[3])
    board.box5.setText(curr_board[4])
    board.box6.setText(curr_board[5])
    board.box7.setText(curr_board[6])
    board.box8.setText(curr_board[7])
    board.box9.setText(curr_board[8])

def BoardGame():
    global board, player_move, playerName
    # Send player name
    while (playerName == "f34h9fvh394vn9fu493oihtnb93yw9yfu9nh49"): { }

    clientGameSocket.sendall(playerName.encode())
    clientChatSocket.sendall(playerName.encode())
    
    board.turn_lbl.setText("Waiting for other player to connect...")
    board.chat_input_box.hide()
    board.send_chat_bt.hide()
    
    #Starting Game
    while True:
        # Playing Game
        while True:
            # Receive current board 
            curr_board = clientGameSocket.recv(BUFFER_SIZE).decode()
            
            board.chat_input_box.show()
            board.send_chat_bt.show()
            
            # Change GUI board to current board
            UpdateBoard(curr_board)
            print(curr_board)
            clientGameSocket.sendall("Received".encode())            
            
            # Check if this is the player's move (1 for yes, 0 for no)
            turn_checker = clientGameSocket.recv(BUFFER_SIZE).decode()
            print("check: " + str(turn_checker) + "\n") #Debugging only
            clientGameSocket.sendall("Received".encode())
            
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
                            clientGameSocket.sendall(player_move.encode())
                            # Check if box is not occupied
                            fill_checker = clientGameSocket.recv(BUFFER_SIZE).decode()
                            clientGameSocket.sendall("Received".encode())
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
                                # input("ERROR 2. Please Exit")
                                raise Exception
                                
                    except(ValueError):
                        board.error_lbl.setText("Please input a number (1-9)")
                        print("Please input a number (1-9)")
                        continue
            else:
                # Should never run. DEBUGGING
                # input("ERROR 1. Please Exit")
                raise Exception
                
            # Check if we should continue
            continue_checker = clientGameSocket.recv(BUFFER_SIZE).decode()
            clientGameSocket.sendall("Received".encode())
            
            if (continue_checker == "Continue"):
                continue
            elif (continue_checker == "Finish"):
                # Update board
                curr_board = clientGameSocket.recv(BUFFER_SIZE).decode()
                clientGameSocket.sendall("Received".encode())
                print(curr_board)
                UpdateBoard(curr_board)
                
                game_message = clientGameSocket.recv(BUFFER_SIZE).decode()
                clientGameSocket.sendall("Received".encode())
                
                current_score = clientGameSocket.recv(BUFFER_SIZE).decode()
                clientGameSocket.sendall("Received".encode())
                board.scoreboard_lbl.setText(current_score)
                print(current_score)
                
                # Show game message
                board.error_lbl.setText(game_message)
                print(game_message)
                
                # Reset turn label
                board.turn_lbl.setText("Next game starting in a few seconds...")
                board.send_move_bt.hide() 
                board.input_edit.hide()
                time.sleep(5)
                board.error_lbl.setText("")
                board.turn_lbl.setText("")
                break
            else:
                # Should never run. DEBUGGING
                # input("ERROR 3. Please Exit")
                raise Exception            

# Chat Functions
def chat_receive():
    # Handles receiving of messages
    global board, playerName
    while (playerName == "f34h9fvh394vn9fu493oihtnb93yw9yfu9nh49"): { }
    while True:
        try:
            message = clientChatSocket.recv(BUFFER_SIZE * 3).decode()
            print(message)
            board.chat_output_box.append(message)
            time.sleep(0.01)
            board.chat_output_box.verticalScrollBar().setValue(board.chat_output_box.verticalScrollBar().maximum())
        except Exception as e:  # Possibly client has left the chat.
            clientChatSocket.close()

if __name__ == "__main__":
    try:
        # Connect with server
        print("Trying to connect..")
        clientGameSocket.connect((HOST, PORT1))
        clientChatSocket.connect((HOST, PORT2))
        print("Connection established!")
        

        game_thread = Thread(target=BoardGame)
        game_thread.start()
        chat_thread = Thread(target=chat_receive)
        chat_thread.start()
        
        app = QApplication(sys.argv)
        board = Board()
        board.show()
        
        app.exec_() 
        
    except Exception as e:
        print("Error!")
        print(str(e) + "\n")
    finally:
        print("Other player has left. Please exit")
        clientGameSocket.close()
        input("Press a key to continue")
       
