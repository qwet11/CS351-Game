import time

# Function to print Tic Tac Toe
def print_tic_tac_toe(values):
    curr_board = "\n" + "\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[0], values[1], values[2]) + "\n\t_____|_____|_____" + "\n\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[3], values[4], values[5]) + "\n\t_____|_____|_____" + "\n\t     |     |" + "\n\t  {}  |  {}  |  {}".format(values[6], values[7], values[8]) + "\n\t     |     |" + "\n"
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
def check_win(player_pos, cur_player):
 
    # All possible winning combinations
    soln = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
 
    # Loop to check if any winning combination is satisfied
    for x in soln:
        if all(y in player_pos[cur_player] for y in x):
 
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
def single_game(piece_letter, curr_socket):
 
    # Represents the Tic Tac Toe
    values = [' ' for x in range(9)]
     
    # Stores the positions occupied by X and O
    player_pos = {'X':[], 'O':[]}
     
    # Game Loop for a single game of Tic Tac Toe
    while True:
        # Send current boards 
        for socket in sockets:
            socket.sendall(print_tic_tac_toe(values).encode())
        print("START SLEEPING\n")
        time.sleep(2) # give enough time for turn_checker
        print("DONE SLEEPING\n")
        # Send 1 or 0 depending on who's turn it is (1 for yes, 0 for no)
        for socket in sockets:
            if (socket == sockets[curr_socket]):
                socket.sendall("1".encode())
            else:
                socket.sendall("0".encode())
        
        time.sleep(5)
        sockets[0].sendall("SENT A WHILE LATER\n")
        #sockets[curr_socket].sendall("Your turn! Which box : ".encode())
        move = int(sockets[curr_socket].recv(BUFFER_SIZE).decode())
 
        # Check if the box is not occupied already (1 for yes, 0 for no)
        if values[move-1] != ' ':
            sockets[curr_socket].sendall("1".encode())
            continue
        else:
            sockets[curr_socket].sendall("0".encode())
 
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
                # Send Won game
                socket.sendall(print_tic_tac_toe(values).encode())
                socket.sendall(("Player " + piece_letter + " has won the game!!").encode())   
            return piece_letter
        # Function call for checking draw game
        elif check_draw(player_pos):
            for socket in sockets:
                # Return a "finish" message (to know that the game is over)
                socket.sendall("Finish".encode())
                # Send Drawn game
                socket.sendall(print_tic_tac_toe(values).encode())
                socket.sendall("Game Drawn".encode())
            return 'D'
        # Return a "continue" message (to know that we continue)
        else:
            for socket in sockets:
                socket.sendall("Continue".encode())
 
        # Switch player moves
        if piece_letter == 'X':
            piece_letter = 'O'
            curr_socket = (curr_socket + 1) % 2
        else:
            piece_letter = 'X'
            curr_socket = (curr_socket + 1) % 2
 
from socket import *

# Server IP Address and Port
HOST = "localhost"
PORT = 65000
BUFFER_SIZE = 1024

# Setting up our socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", PORT))
serverSocket.listen()

while True:
    try:
        # Establish connection with client 1
        print("Waiting for player 1...")
        connectionSocket1, connectionAddress1 = serverSocket.accept()
        print("Player 1 connected successful!\n")
        
        # Establish connection with client 2
        print("Waiting for player 2...")
        connectionSocket2, connectionAddress2 = serverSocket.accept()
        print("Player 2 connected successfully!\n")
        
        # Get players names
        player1 = connectionSocket1.recv(BUFFER_SIZE).decode()
        player2 = connectionSocket2.recv(BUFFER_SIZE).decode()
        
        # Stores the current player
        cur_player = player1
        
        # Stores the choice of players 
        player_choice = {"X" : "", "O" : ""}
        
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
        
        # Send current scoreboard
        #for socket in sockets:
        #    socket.sendall(print_scoreboard(score_board).encode())
        
        # Game Loop for a series of Tic Tac Toe
        # The loop runs until the players quit 
        while True:
            # Stores the winner in a single game of Tic Tac Toe
            winner = single_game(options[0], curr_socket)
             
            # Edits the scoreboard according to the winner
            if winner != 'D' :
                player_won = player_choice[winner]
                score_board[player_won] = score_board[player_won] + 1
            
            for socket in sockets:
                socket.sendall(print_scoreboard(score_board).encode())
                
            # Switch player who chooses X or O
            if cur_player == player1:
                cur_player = player2
                curr_socket = 1
            else:
                cur_player = player1
                curr_socket = 0
    except Exception as e:
        print("Error!")
        print(str(e) + "\n")
    finally:
        # Close connection with client
        for socket in sockets:
            socket.close()
        print("Connection successfully terminated!\n")
        

