from threading import Thread
from socket import *

# For debugging only
def print_error_message(message, label):
    print(message)
    print("Label: ", label)
    input("Please Exit!")

# Function to print Tic Tac Toe
def print_tic_tac_toe(values):
    curr_board = ""
    for value in values:
        curr_board += value
    # curr_board = "\n" + "\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[0], values[1], values[2]) + "\n\t_____|_____|_____" + "\n\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[3], values[4], values[5]) + "\n\t_____|_____|_____" + "\n\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[6], values[7], values[8]) + "\n\t     |     |" + "\n"
    return curr_board
 
 
# Function to print the score-board
def print_scoreboard(score_board):
    curr_scoreboard = "\t--------------------------------" + "\n\t SCOREBOARD       " + "\n\t--------------------------------\n"
 
    players = list(score_board.keys())
    curr_scoreboard += ("\t   ", players[0], "\t    ", score_board[players[0]] + "\n")
    curr_scoreboard += ("\t   ", players[1], "\t    ", score_board[players[1]] + "\n")
    curr_scoreboard += ("\t--------------------------------\n")
    return curr_scoreboard
 
# Function to check if any player has won
def check_win(player_pos, curr_player):
 
    # All possible winning combinations
    soln = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
 
    # Loop to check if any winning combination is satisfied
    for x in soln:
        if all(y in player_pos[curr_player] for y in x):
 
            # Return True if any winning combination satisfies
            return True
    # Return False if no combination is satisfied       
    return False       
 
# Function to check if the game is drawn
def check_draw(player_pos):
    if len(player_pos['X']) + len(player_pos['O']) == 9:
        return True
    return False       
 
# Function for a single game of Tic Tac Toe
def single_game(piece_letter, player_choice, curr_socket, sockets):
    global score_board
    
    # Represents the Tic Tac Toe
    values = [' ' for x in range(9)]
     
    # Stores the positions occupied by X and O
    player_pos = {'X':[], 'O':[]}
     
    # Game Loop for a single game of Tic Tac Toe
    while True:
        # Send current boards 
        for socket in sockets:
            socket.sendall(print_tic_tac_toe(values).encode())
            if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 100)
        
        # Send 1 or 0 depending on who's turn it is (1 for yes, 0 for no)
        for socket in sockets:
            if (socket == sockets[curr_socket]):
                socket.sendall("1".encode())
            else:
                socket.sendall("0".encode())
                
            if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 200)
        
        while True: 
            move = int(sockets[curr_socket].recv(BUFFER_SIZE).decode())
     
            # Check if the box is not occupied already (1 for yes, 0 for no)
            if values[move-1] != ' ':
                sockets[curr_socket].sendall("1".encode())
                if (sockets[curr_socket].recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 300)
                continue
            else:
                sockets[curr_socket].sendall("0".encode())
                if (sockets[curr_socket].recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 400)
                break
 
        # Update game information
 
        # Updating grid status 
        values[move-1] = piece_letter
 
        # Updating player positions
        player_pos[piece_letter].append(move)
 
        # Function call for checking win
        if check_win(player_pos, piece_letter):
            for socket in sockets:
                # Return a "finish" message (to know that the game is over)
                socket.sendall("Finish".encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 500)
                    
                # Send Won game
                socket.sendall(print_tic_tac_toe(values).encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 600)
                
                socket.sendall((player_choice[piece_letter] + " has won the game!!").encode())   
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 700)
                    
                    
            return piece_letter
        # Function call for checking draw game
        elif check_draw(player_pos):
            for socket in sockets:
                # Return a "finish" message (to know that the game is over)
                socket.sendall("Finish".encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 800)
                    
                # Send Drawn game
                socket.sendall(print_tic_tac_toe(values).encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 900)
                    
                socket.sendall("Game Drawn".encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 1000)
            return 'D'
        # Return a "continue" message (to know that we continue)
        else:
            for socket in sockets:
                socket.sendall("Continue".encode())
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 1100)
                
        # Switch player moves
        if piece_letter == 'X':
            piece_letter = 'O'
            curr_socket = (curr_socket + 1) % 2
        else:
            piece_letter = 'X'
            curr_socket = (curr_socket + 1) % 2
 
# Connect clients
def pair_incoming_clients():
    while True:
    # ====Put into function for threading====
        try:
            # Establish connection with client 1
            print("Waiting for player 1...")
            connectionSocket1, connectionAddress1 = serverGameSocket.accept()
            connectionChatSocket1, connectionChatAddress1 = serverChatSocket.accept()
            print("Player 1 connected successful!\n")
            
            # Establish connection with client 2
            print("Waiting for player 2...")
            connectionSocket2, connectionAddress2 = serverGameSocket.accept()
            connectionChatSocket2, connectionChatAddress2 = serverChatSocket.accept()
            print("Player 2 connected successfully!\n")
            
            Thread(target=play_game_room, args=(connectionSocket1, connectionSocket2)).start()
            Thread(target=handle_chat, args=(connectionChatSocket1, connectionChatSocket2)).start()
            Thread(target=handle_chat, args=(connectionChatSocket2, connectionChatSocket1)).start()
            
        except socket.error:
            connectionSocket1.close()
            connectionSocket2.close()
        
        except Exception as e:
            # print("Error!")
            # print(str(e) + "\n")
            connectionSocket1.close()
            connectionSocket2.close()
            
        """"
        finally:
            # Close connection with client
            for socket in sockets:
                socket.close()
            print("Connection successfully terminated!\n")
        """
        
def play_game_room(connectionSocket1, connectionSocket2):
    global score_board
    try: 
        # Get players names
        player1 = connectionSocket1.recv(BUFFER_SIZE).decode()[:11]
        player2 = connectionSocket2.recv(BUFFER_SIZE).decode()[:11]
        
        # Stores the current player
        curr_player = player1
        
        # Stores the choice of players 
        player_choice = {"X" : player1, "O" : player2}
        
        # Stores the options 
        options = ["X", "O"]
        
        # May change
        player_choice["X"] = player1
        player_choice["O"] = player2
        
        # Stores the scoreboard
        score_board = {player1 : 0, player2: 0}
        
        # Stores the sockets
        sockets = [connectionSocket1, connectionSocket2]
        
        # Stores the current socket index (for the current player)
        curr_socket = 0
        
        """
        # Send current scoreboard
        for socket in sockets:
            socket.sendall(print_scoreboard(score_board).encode())
        """
        
        # Game Loop for a series of Tic Tac Toe
        # The loop runs until the players quit 
        while True:
            # Stores the winner in a single game of Tic Tac Toe
            winner = single_game(options[curr_socket], player_choice, curr_socket, sockets)
             
            # Edits the scoreboard according to the winner
            if winner != 'D' :
                player_won = player_choice[winner]
                score_board[player_won] = score_board[player_won] + 1
            
            """
            for socket in sockets:
                socket.sendall(print_scoreboard(score_board).encode())
            """
            for socket in sockets:
                # score_board[winner] = score_board[winner] + 1
                socket.sendall(("%s: %d     %s: %d" % (player_choice['X'], score_board[player_choice['X']], player_choice['O'], score_board[player_choice['O']])).encode())   
                if (socket.recv(BUFFER_SIZE).decode() != "Received"):
                    print_error_message("ERROR. Out of Sync", 1200)
            
            # Switch player who chooses X or O
            if curr_player == player1:
                curr_player = player2
                curr_socket = 1
            else:
                curr_player = player1
                curr_socket = 0
                
    except Exception as e:
        connectionSocket1.close()
        connectionSocket2.close()
        # Thread.exit()
        # print("Players Left")
        # print(str(e) + "\n")
        
def handle_chat(clientSocket, pairSocket):
    try:
        chatName = clientSocket.recv(BUFFER_SIZE).decode()[:11]
        broadcast(("%s has joined the chat!" % chatName), chatName, clientSocket, pairSocket) 
    
        while True:
            message = clientSocket.recv(BUFFER_SIZE * 3).decode()
            broadcast(message, chatName, clientSocket, pairSocket)
    except Exception as e:
        clientSocket.close()
        pairSocket.close()

def broadcast(message, name, socket1, socket2):
    # Broadcasts a message to all the clients

    socket1.sendall(("%s: %s \n" % (name, message)).encode())
    socket2.sendall(("%s: %s \n" % (name, message)).encode())

if __name__ == "__main__":
    # Server IP Address and Port
    HOST = "localhost"
    PORT1 = 64000
    PORT2 = 65000
    BUFFER_SIZE = 1024
    
    # Setting up our sockets
    serverGameSocket = socket(AF_INET, SOCK_STREAM)
    serverGameSocket.bind((HOST, PORT1))
    serverGameSocket.listen(40)
    
    serverChatSocket = socket(AF_INET, SOCK_STREAM)
    serverChatSocket.bind((HOST, PORT2))
    serverChatSocket.listen(40)
    
    accept_thread = Thread(target=pair_incoming_clients)
    accept_thread.start()
    accept_thread.join()
    serverGameSocket.close()
    serverChatSocket.close()

