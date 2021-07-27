########## TIC TAC TOE ##########

import random


########## FUNCTIONS ##########


# print tic-tac-toe board with given configuration
def print_board(board):
    for i in range(7):  # rows 0-6
        for j in range(12):  # columns 0-11

            # row/col labels
            if (i == 1 or i == 3 or i == 5) and j == 0:
                print(int((i + 1) / 2), end="")
            if i == 0 and (j == 2 or j == 6 or j == 10):
                print(int((j + 2) / 4), end="")
            # blank space
            if (i == 2 or i == 4 or i == 6) and j == 0:
                print(" ", end="")

            # horizontal lines
            if (i == 2 or i == 4) and j != 0 and j != 4 and j != 8:
                print("_", end='')

            # vertical lines
            elif i != 0 and (j == 4 or j == 8):
                print("|", end='')

            # block information
            elif (i == 1 or i == 3 or i == 5) and (j == 2 or j == 6 or j == 10):
                print(board[int((i - 1) / 2)][int((j - 2) / 4)], end='')
            else:
                print(" ", end='')

            # new line
            if j == 11:
                print("")


# returns opposite symbol
def opposite_symbol(symbol):
    if symbol == 'X':
        return 'O'
    return 'X'


# randomly choose first player
def who_goes_first(player, computer):
    if random.choice(['O', 'X']) == player:
        print("You (" + player + ") can make the first move.")
        return player
    else:
        print("The computer (" + computer + ") will make the first move.")
        return computer


# check if valid move (within bounds & unoccupied)
def valid_move(row, col, board):
    valid = True
    if row < 0 or row > 2 or col < 0 or col > 2:
        valid = False
    if board[row][col] != ' ':
        valid = False
    return valid


# player's move
def player_move(symbol, board):
    # ask to make move (x and y coordinates) until valid
    move_made = False
    while not move_made:
        move = input("Enter move for " + player + " (RowCol): ")
        row = int(move[0]) - 1
        col = int(move[1]) - 1

        if valid_move(row, col, board):
            board[row][col] = player
            print_board(board)
            move_made = True
        else:
            print("Invalid move.")


# count number of blank spaces
def count_blank_spaces(board):
    blank_spaces = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                blank_spaces += 1
    return blank_spaces


# spot and score winning move(s)
def winning_move(row, col, symbol, board):
    winning_potential = 0

    if not valid_move(row, col, board):
        winning_potential -= 20

    else:
        # horizontal
        if col == 0:
            if board[row][1] == symbol and board[row][2] == symbol:
                winning_potential += 20
        elif col == 1:
            if board[row][0] == symbol and board[row][2] == symbol:
                winning_potential += 20
        else:
            if board[row][0] == symbol and board[row][1] == symbol:
                winning_potential += 20
        # vertical
        if row == 0:
            if board[1][col] == symbol and board[2][col] == symbol:
                winning_potential += 20
        elif row == 1:
            if board[0][col] == symbol and board[2][col] == symbol:
                winning_potential += 20
        else:
            if board[0][col] == symbol and board[1][col] == symbol:
                winning_potential += 20
        # diagonal
        if row == 0:
            if (col == 0 and board[1][1] == symbol and board[2][2] == symbol) or (
                    col == 2 and board[1][1] == symbol and board[2][0] == symbol):
                winning_potential += 20
        elif row == 1 and col == 1:
            if (board[0][0] == symbol and board[2][2] == symbol) or (board[0][2] == symbol and board[2][0] == symbol):
                winning_potential += 20
        elif row == 2:
            if (col == 2 and board[0][0] == symbol and board[1][1] == symbol) or (
                    col == 0 and board[0][2] == symbol and board[1][1] == symbol):
                winning_potential += 20
    return winning_potential


# help computer choose move by scoring each space
def score_move(row, col, symbol, board):
    score = 0

    # invalid move
    if not valid_move(row, col, board):
        score -= 1

    # positive scores only attributed to valid moves (unoccupied and on board)
    else:
        # WINNING MOVE (priority)
        score += winning_move(row, col, symbol, board) + 20
        # BLOCK WINNING MOVE
        score += winning_move(row, col, opposite_symbol(symbol), board)

        # SMART WINS
        # first row
        if row == 0:
            # vertical
            if board[row + 1][col] == symbol or board[row + 2][col] == symbol:
                score += 5
            # vertical/diagonal - consider bounds
            if col == 0:
                # horizontal
                if board[row][col + 1] == symbol or board[row][col + 2] == symbol:
                    score += 5
                # diagonal (top-right to bottom-left)
                if board[row + 1][col + 1] == symbol or board[row + 2][col + 2] == symbol:
                    score += 5
            elif col == 1:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col + 1] == symbol:
                    score += 5
            else:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col - 2] == symbol:
                    score += 5
                # diagonal (top-left to bottom-right)
                if board[row + 1][col - 1] == symbol or board[row + 2][col - 2] == symbol:
                    score += 5

        # second row
        elif row == 1:
            # vertical
            if board[row - 1][col] == symbol or board[row + 1][col] == symbol:
                score += 5
            # vertical/diagonal - consider bounds
            if col == 0:
                # horizontal
                if board[row][col + 1] == symbol or board[row][col + 2] == symbol:
                    score += 5
            elif col == 1:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col + 1] == symbol:
                    score += 5
                # diagonal (both)
                if board[row - 1][col - 1] == symbol or board[row + 1][col + 1] == symbol or \
                        board[row - 1][col + 1] == symbol or board[row + 1][col - 1] == symbol:
                    score += 5
            else:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col - 2] == symbol:
                    score += 5

        # third row (row == 2)
        else:
            # vertical
            if board[row - 1][col] == symbol or board[row - 2][col] == symbol:
                score += 5
            # vertical/diagonal - consider bounds
            if col == 0:
                # horizontal
                if board[row][col + 1] == symbol or board[row][col + 2] == symbol:
                    score += 5
                # diagonal (top-left to bottom-right)
                if board[row - 1][col + 1] == symbol or board[row - 2][col + 2] == symbol:
                    score += 5
            elif col == 1:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col + 1] == symbol:
                    score += 5
            else:
                # horizontal
                if board[row][col - 1] == symbol or board[row][col - 2] == symbol:
                    score += 5
                # diagonal (top-left to bottom-right)
                if board[row - 1][col - 1] == symbol or board[row - 2][col - 2] == symbol:
                    score += 5

    return score


# AI for the computer's move
def computer_move(symbol, board):

    # computer = 'X' (first move) or computer = '0' (second move w empty corners)
    if count_blank_spaces(board) == 9 or (count_blank_spaces(board) == 8 and board[0][0] != opposite_symbol(symbol) and
                                          board[0][2] != opposite_symbol(symbol) and board[2][0] != opposite_symbol(symbol) and
                                          board[2][2] != opposite_symbol(symbol)):
        row = random.choice([0, 2])
        col = random.choice([0, 2])
        board[row][col] = symbol
        return
    # computer = '0' (place in centre if opponent placed in corner in first move)
    elif count_blank_spaces(board) == 8 and (board[0][0] == opposite_symbol(symbol) or board[0][2] == opposite_symbol(symbol) or
                                           board[2][0] == opposite_symbol(symbol) or board[2][2] == opposite_symbol(symbol)):
            board[1][1] = symbol
            return

    # use scoring AI to determine rest of moves
    if count_blank_spaces(board) < 8:
        high_score = 0
        high_row = 0
        high_col = 0

        for i in range(3):
            for j in range(3):
                move_score = score_move(i, j, symbol, board)

                # to check scoring of spaces
                # print(str(i) + str(j) + ": " + str(move_score))

                if move_score >= high_score:
                    high_score = move_score
                    high_row = i
                    high_col = j

        board[high_row][high_col] = symbol
        return


# check for available moves
def available_moves(board):
    empty_blocks = 0
    for row in range(3):
        for col in range(3):
            if board[row - 1][col - 1] == " ":
                empty_blocks += 1
    return empty_blocks


# determine winner/draw
def determine_outcome(turn, player, board):
    outcome = True

    # OUTCOME
    # horizontal
    for row in range(3):
        if board[row][0] == turn and board[row][1] == turn and board[row][2] == turn:
            if turn == player:
                print("You win!")
            else:
                print("You lose!")
            return outcome
    # vertical
    for col in range(3):
        if board[0][col] == turn and board[1][col] == turn and board[2][col] == turn:
            if turn == player:
                print("You win!")
            else:
                print("You lose!")
            return outcome
    # diagonal (top-left to bottom-right)
    if board[0][0] == turn and board[1][1] == turn and board[2][2] == turn:
        if turn == player:
            print("You win!")
        else:
            print("You lose!")
        return outcome
    # diagonal (top-right to bottom-left)
    if board[0][2] == turn and board[1][1] == turn and board[2][0] == turn:
        if turn == player:
            print("You win!")
        else:
            print("You lose!")
        return outcome

    # NO outcome from hereon
    # no more available moves, DRAW
    if not available_moves(board):
        print("Draw!")
        return outcome

    # CONTINUE GAME
    else:
        outcome = False

    return outcome


########## MAIN CODE ##########

game = True

# initial state of board
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

# introduce game and assign symbols
print("You are playing Tic-Tac-Toe.")
print_board(board)
player = input("Please pick a symbol ('X' or 'O'): ")
computer = opposite_symbol(player)
turn = who_goes_first(player, computer)

# play game until GAME OVER (game == false)
while game:

    # if player's turn
    if turn == player:
        player_move(turn, board)

    # if computer's turn
    elif turn == computer:
        computer_move(turn, board)
        print("The computer (" + computer + ") made its move.")
        print_board(board)

    # switching turns or ending game
    # if there are available moves AND no one won yet
    if available_moves(board) > 0 and not determine_outcome(turn, player, board):
        turn = opposite_symbol(turn)
    else:
        determine_outcome(turn, player, board)
        game = False
