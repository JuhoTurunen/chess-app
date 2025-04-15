# pylint: skip-file

import unittest
from entities.board import Board
from services.game_service import GameService


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.board = Board("white")
        self.game_service = GameService(self.board)

    def test_pawn_move(self):
        self.assertTrue(self.game_service.move_handler(((6, 2), (5, 2))))

    def test_pawn_can_jump(self):
        self.assertTrue(self.game_service.move_handler(((6, 2), (4, 2))))

    def test_pawn_loses_jump_ability(self):
        self.game_service.move_handler(((6, 2), (4, 2)))
        self.game_service.move_handler(((6, 0), (5, 0)))

        self.assertFalse(self.game_service.move_handler(((4, 2), (2, 2))))
        self.assertFalse(self.game_service.move_handler(((5, 2), (3, 2))))

    def test_pawn_can_diagonal_eat(self):
        self.assertTrue(self.game_service.move_handler(((6, 3), (4, 3))))
        self.assertTrue(self.game_service.move_handler(((6, 3), (4, 3))))

        self.assertTrue(self.game_service.move_handler(((4, 3), (3, 4))))

        self.assertEqual(self.game_service.board.get_piece((3, 4)), None)
        self.assertEqual(self.game_service.board.get_piece((4, 3)).__repr__(), "wP")

    def test_pawn_cant_diagonal_move(self):
        self.assertFalse(self.game_service.move_handler(((6, 2), (5, 3))))

    def test_pawn_cant_forward_eat(self):
        self.assertTrue(self.game_service.move_handler(((6, 4), (4, 4))))
        self.assertTrue(self.game_service.move_handler(((6, 3), (4, 3))))

        self.assertFalse(self.game_service.move_handler(((4, 4), (3, 4))))

        self.assertEqual(self.game_service.board.get_piece((3, 4)).__repr__(), "bP")
        self.assertEqual(self.game_service.board.get_piece((4, 4)).__repr__(), "wP")
