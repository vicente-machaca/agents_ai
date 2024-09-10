#!/usr/bin/python

"""
Python implementation of text-mode version of the Tetris game

Quick play instructions:

 - a (return): move piece left
 - d (return): move piece right
 - w (return): rotate piece counter clockwise
 - s (return): rotate piece clockwise
 - e (return): just move the piece downwards as is
 - q (return): quit the game

"""

import os
import random
import sys
from copy import deepcopy

# Constants
BOARD_SIZE = 20
EFF_BOARD_SIZE = BOARD_SIZE + 2
PIECES = [[[1], [1], [1], [1]],     [[1, 0], [1, 0], [1, 1]],     [[0, 1], [0, 1], [1, 1]],     [[0, 1], [1, 1], [1, 0]],     [[1, 1], [1, 1]]]
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
ROTATE_ANTICLOCKWISE = 'w'
ROTATE_CLOCKWISE = 's'
NO_MOVE = 'e'
QUIT_GAME = 'q'

class Board:
    def __init__(self):
        self.board = [[0] * EFF_BOARD_SIZE for _ in range(EFF_BOARD_SIZE)]
        self._create_walls()

    def _create_walls(self):
        for i in range(EFF_BOARD_SIZE):
            self.board[0][i] = 1
            self.board[EFF_BOARD_SIZE - 1][i] = 1
            self.board[i][0] = 1
            self.board[i][EFF_BOARD_SIZE - 1] = 1

    def can_move(self, piece, pos):
        piece_size_x = len(piece.shape)
        piece_size_y = len(piece.shape[0])
        for i in range(piece_size_x):
            for j in range(piece_size_y):
                if (pos[0] + i >= EFF_BOARD_SIZE or pos[1] + j >= EFF_BOARD_SIZE or
                        self.board[pos[0] + i][pos[1] + j] == 1 and piece.shape[i][j] == 1):
                    return False
        return True

    def add_piece(self, piece, pos):
        piece_size_x = len(piece.shape)
        piece_size_y = len(piece.shape[0])
        for i in range(piece_size_x):
            for j in range(piece_size_y):
                if piece.shape[i][j] == 1:
                    self.board[pos[0] + i][pos[1] + j] = 1
        self.clear_rows()

    def clear_rows(self):
        for i in range(1, EFF_BOARD_SIZE - 1):
            if all(self.board[i][j] == 1 for j in range(1, EFF_BOARD_SIZE - 1)):
                for k in range(i, 1, -1):
                    self.board[k] = deepcopy(self.board[k - 1])
                self.board[1] = [1] + [0] * (EFF_BOARD_SIZE - 2) + [1]

    def display(self, piece=None, pos=None, error_message=''):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Text mode version of the TETRIS game

")
        board_copy = deepcopy(self.board)
        if piece and pos:
            piece_size_x = len(piece.shape)
            piece_size_y = len(piece.shape[0])
            for i in range(piece_size_x):
                for j in range(piece_size_y):
                    board_copy[pos[0] + i][pos[1] + j] |= piece.shape[i][j]
        for row in board_copy:
            for cell in row:
                print("*" if cell == 1 else " ", end='')
            print()
        print("

" + error_message)
        print("Instructions: a (left), d (right), w (rotate ccw), s (rotate cw), e (drop), q (quit)")

class Piece:
    def __init__(self, shape):
        self.shape = shape

    def rotate_clockwise(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def rotate_anticlockwise(self):
        self.shape = [list(row) for row in zip(*self.shape)][::-1]

class Tetris:
    def __init__(self):
        self.board = Board()
        self.current_piece = self.random_piece()
        self.piece_position = [1, EFF_BOARD_SIZE // 2]

    def random_piece(self):
        return Piece(random.choice(PIECES))

    def play(self):
        while True:
            self.board.display(self.current_piece, self.piece_position)
            move = input().strip()
            if move == QUIT_GAME:
                break
            self.process_move(move)
        print("Game Over!")

    def process_move(self, move):
        if move == MOVE_LEFT:
            new_pos = [self.piece_position[0], self.piece_position[1] - 1]
        elif move == MOVE_RIGHT:
            new_pos = [self.piece_position[0], self.piece_position[1] + 1]
        elif move == ROTATE_CLOCKWISE:
            self.current_piece.rotate_clockwise()
            new_pos = self.piece_position
        elif move == ROTATE_ANTICLOCKWISE:
            self.current_piece.rotate_anticlockwise()
            new_pos = self.piece_position
        elif move == NO_MOVE:
            while self.board.can_move(self.current_piece, [self.piece_position[0] + 1, self.piece_position[1]]):
                self.piece_position[0] += 1
            self.board.add_piece(self.current_piece, self.piece_position)
            self.current_piece = self.random_piece()
            self.piece_position = [1, EFF_BOARD_SIZE // 2]
            return
        else:
            new_pos = self.piece_position
        if self.board.can_move(self.current_piece, new_pos):
            self.piece_position = new_pos
        else:
            if move in [ROTATE_CLOCKWISE, ROTATE_ANTICLOCKWISE]:
                # If rotation is not possible, rotate back
                if move == ROTATE_CLOCKWISE:
                    self.current_piece.rotate_anticlockwise()
                else:
                    self.current_piece.rotate_clockwise()

if __name__ == "__main__":
    Tetris().play()
