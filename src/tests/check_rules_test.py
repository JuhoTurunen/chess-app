# pylint: skip-file

import unittest
from entities.board import Board
from services.move_simulator import simulate_move


class TestKingCheck(unittest.TestCase):
    def test_disallow_normal_moves_in_check(self):
        board = Board("black")

        # Pass if not threatened
        self.assertTrue(simulate_move(board, ((6, 0), (5, 0))))

        enemy_rook = board.get_piece((0, 0))
        board.set_piece((6, 3), enemy_rook)

        # Don't pass if threatened
        self.assertFalse(simulate_move(board, ((6, 0), (5, 0))))
