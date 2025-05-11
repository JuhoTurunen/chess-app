# pylint: skip-file

import unittest
from engine.entities.board import Board
from engine.services.game_service import GameService


class TestGameEnd(unittest.TestCase):
    def setUp(self):
        self.board = Board("black")
        self.game_service = GameService(self.board)

    def test_black_win(self):
        self.assertTrue(self.game_service.move_handler(((6, 5), (5, 5))))
        self.assertTrue(self.game_service.move_handler(((6, 3), (5, 3))))
        self.assertTrue(self.game_service.move_handler(((6, 6), (4, 6))))
        
        self.assertEqual(self.game_service.get_winner(), None)
        self.assertTrue(self.game_service.move_handler(((7, 4), (3, 0))))
        self.assertEqual(self.game_service.get_winner(), "black")
    
    def test_stall_clock_counter(self):
        self.assertEqual(self.game_service.board.stall_clock, 0)
        self.assertTrue(self.game_service.move_handler(((6, 5), (5, 5))))
        self.assertEqual(self.game_service.board.stall_clock, 0)
        self.assertTrue(self.game_service.move_handler(((7, 1), (5, 0))))
        self.assertEqual(self.game_service.board.stall_clock, 1)
    
    def test_stall_draw(self):
        self.game_service.board.stall_clock = 49
        self.assertTrue(self.game_service.move_handler(((7, 1), (5, 0))))
        self.assertEqual(self.game_service.board.stall_clock, 50)
        self.assertEqual(self.game_service.get_winner(), "draw")
