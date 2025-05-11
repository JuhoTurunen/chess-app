# pylint: skip-file

import unittest
from engine.entities.board import Board
from engine.services.core.move_simulator import simulate_move
from engine.services.ai_engine import AiEngine


class TestAiEngine(unittest.TestCase):
    def setUp(self):
        self.ai_engine = AiEngine(2)

    def test_get_best_move_returns_valid_move(self):
        board = Board("white")
        ai_move = self.ai_engine.get_best_move(board)
        self.assertTrue(simulate_move(board, ai_move))
