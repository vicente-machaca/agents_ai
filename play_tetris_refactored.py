import os
import random
import sys
from copy import deepcopy

# Constants
BOARD_SIZE = 20
EFF_BOARD_SIZE = BOARD_SIZE + 2
PIECES = [
    [[1], [1], [1], [1]],
    [[1, 0], [1, 0], [1, 1]],
    [[0, 1], [0, 1], [1, 1]],
    [[0, 1], [1, 1], [1, 0]],
    [[1, 1], [1, 1]]
]

MOVES = {
    'LEFT': 'a',
    'RIGHT': 'd',
    'ROTATE_ANTICLOCKWISE': 'w',
    'ROTATE_CLOCKWISE': 's',
    'NO_MOVE': 'e',
    'QUIT': 'q'
}


def print_board(board, curr_piece, piece_pos, error_message=''):
    """
    Print the Tetris game board to the console.

    Parameters:
    - board: The game board matrix.
    - curr_piece: The current active piece.
    - piece_pos: The top-left position of the active piece on the board.
    - error_message: Any error message to display.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Text mode version of the TETRIS game\n\n")

    board_copy = deepcopy(board)
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])

    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            board_copy[piece_pos[0] + i][piece_pos[1] + j] |= curr_piece[i][j]

    for i in range(EFF_BOARD_SIZE):
        for j in range(EFF_BOARD_SIZE):
            print("*" if board_copy[i][j] else " ", end='')
        print()

    print(error_message)
    print("\nInstructions: a-LEFT d-RIGHT w-ROTATE_ANTICW s-ROTATE_CW e-NO_MOVE q-QUIT")


def initialize_board():
    """
    Initialize the game board with walls.

    Returns:
    - A matrix representing the initialized game board.
    """
    board = [[0] * EFF_BOARD_SIZE for _ in range(EFF_BOARD_SIZE)]
    
    for i in range(EFF_BOARD_SIZE):
        board[0][i] = 1
        board[EFF_BOARD_SIZE - 1][i] = 1
        board[i][0] = 1
        board[i][EFF_BOARD_SIZE - 1] = 1
    
    return board


def check_collision(board, piece, pos):
    """
    Check if the piece collides with the board.

    Parameters:
    - board: The game board matrix.
    - piece: The current piece matrix.
    - pos: The top-left position to check for collision.

    Returns:
    - True if there's a collision, False otherwise.
    """
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] and board[pos[0] + i][pos[1] + j]:
                return True
    return False


def clear_full_lines(board):
    """
    Remove complete lines from the board and return the new board.

    Parameters:
    - board: The game board matrix.

    Returns:
    - The new game board matrix after clearing full lines.
    """
    new_board = deepcopy(board)
    
    lines_to_clear = [i for i in range(1, EFF_BOARD_SIZE - 1) if all(new_board[i][j] for j in range(1, EFF_BOARD_SIZE - 1))]
    
    for line in lines_to_clear:
        del new_board[line]
        new_board.insert(1, [1] + [0] * (BOARD_SIZE) + [1])
    
    return new_board


def rotate_piece(piece, clockwise=True):
    """
    Rotate the piece matrix.

    Parameters:
    - piece: The current piece matrix.
    - clockwise: Rotate clockwise if True, counter-clockwise otherwise.

    Returns:
    - The rotated piece matrix.
    """
    if clockwise:
        return [list(x)[::-1] for x in zip(*piece)]
    return [list(x) for x in zip(*piece[::-1])][::-1]


def main():
    """
    Main function to run the Tetris game.
    """
    board = initialize_board()
    curr_piece = random.choice(PIECES)
    piece_pos = [1, EFF_BOARD_SIZE // 2 - len(curr_piece[0]) // 2]

    while True:
        error_message = ''
        print_board(board, curr_piece, piece_pos)
        move = input("Enter your move: ")

        if move == MOVES['QUIT']:
            print("Game Over!")
            break

        next_piece_pos = piece_pos[:]
        next_piece = curr_piece
        if move == MOVES['LEFT']:
            next_piece_pos[1] -= 1
        elif move == MOVES['RIGHT']:
            next_piece_pos[1] += 1
        elif move == MOVES['ROTATE_ANTICLOCKWISE']:
            next_piece = rotate_piece(curr_piece, clockwise=False)
        elif move == MOVES['ROTATE_CLOCKWISE']:
            next_piece = rotate_piece(curr_piece, clockwise=True)
        elif move == MOVES['NO_MOVE']:
            next_piece_pos[0] += 1
        else:
            error_message = "Invalid move!"

        if not check_collision(board, next_piece, next_piece_pos):
            curr_piece = next_piece
            piece_pos = next_piece_pos
        else:
            if move == MOVES['NO_MOVE']:
                for i in range(len(curr_piece)):
                    for j in range(len(curr_piece[0])):
                        board[piece_pos[0] + i][piece_pos[1] + j] |= curr_piece[i][j]
                board = clear_full_lines(board)
                curr_piece = random.choice(PIECES)
                piece_pos = [1, EFF_BOARD_SIZE // 2 - len(curr_piece[0]) // 2]
                if check_collision(board, curr_piece, piece_pos):
                    print_board(board, curr_piece, piece_pos, "GAME OVER!")
                    break
        print_board(board, curr_piece, piece_pos, error_message)

if __name__ == "__main__":
    main()
