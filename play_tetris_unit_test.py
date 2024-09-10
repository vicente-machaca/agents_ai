import unittest
from copy import deepcopy
from play_tetris_refactored import initialize_board, check_collision, clear_full_lines, rotate_piece, PIECES, EFF_BOARD_SIZE, BOARD_SIZE


class TestTetris(unittest.TestCase):

    def test_initialize_board(self):
        board = initialize_board()
        self.assertEqual(len(board), EFF_BOARD_SIZE)
        self.assertEqual(len(board[0]), EFF_BOARD_SIZE)
        for i in range(EFF_BOARD_SIZE):
            self.assertEqual(board[0][i], 1)
            self.assertEqual(board[EFF_BOARD_SIZE - 1][i], 1)
            self.assertEqual(board[i][0], 1)
            self.assertEqual(board[i][EFF_BOARD_SIZE - 1], 1)
    
    def test_check_collision(self):
        board = initialize_board()
        piece = PIECES[0]  # [[1], [1], [1], [1]]
        pos = [1, 1]
        self.assertFalse(check_collision(board, piece, pos))
        pos = [0, 0]
        self.assertTrue(check_collision(board, piece, pos))
    
    def test_clear_full_lines(self):
        board = initialize_board()
        for i in range(1, EFF_BOARD_SIZE - 1):
            board[i][1:BOARD_SIZE + 1] = [1] * BOARD_SIZE
        new_board = clear_full_lines(board)
        empty_line = [1] + [0] * BOARD_SIZE + [1]
        for i in range(1, EFF_BOARD_SIZE - 1):
            self.assertEqual(new_board[i], empty_line)
    
    def test_rotate_piece(self):
        piece = PIECES[1]  # [[1, 0], [1, 0], [1, 1]]
        rotated_clockwise = rotate_piece(piece, clockwise=True)
        expected_clockwise = [[1, 1, 1], [1, 0, 0]]
        self.assertEqual(rotated_clockwise, expected_clockwise)
        
        rotated_counterclockwise = rotate_piece(piece, clockwise=False)
        expected_counterclockwise = [[0, 0, 1], [1, 1, 1]]
        self.assertEqual(rotated_counterclockwise, expected_counterclockwise)


if __name__ == '__main__':
    unittest.main()
