# pylint: skip-file

import unittest
from engine.entities.board import Board
from engine.services.ai_engine import AiEngine
from engine.services.game_service import GameService


class TestAiEngine(unittest.TestCase):
    def setUp(self):
        self.board = Board("white")
        self.game_service = GameService(self.board)

    def test_get_best_move_returns_valid_move(self):
        ai_engine = AiEngine(2)
        ai_move = ai_engine.get_best_move(self.board)
        self.assertTrue(self.game_service.move_handler(ai_move))

    def test_ai_executes_mate_in_two(self):
        for row in range(8):
            for col in range(8):
                self.game_service.board.set_piece((row, col), None)

        # Position with checkmate by white in two moves:
        # If mate in two is not taken, white will lose in one move.
        #
        #    -- -- -- -- -- -- -- --
        #    -- -- -- wP -- -- bP bK
        #    -- -- -- -- -- -- -- bP
        #    -- -- -- -- -- wP -- wB
        #    -- -- -- -- -- -- -- --
        #    -- -- bQ -- -- -- -- --
        #    -- wP bQ -- -- -- -- --
        #    -- -- -- -- -- -- -- wK

        # Black pieces
        self.game_service.board.set_piece((1, 7), ("black", "king", True))
        self.game_service.board.set_piece((5, 2), ("black", "queen", False))
        self.game_service.board.set_piece((6, 2), ("black", "queen", False))
        self.game_service.board.set_piece((1, 6), ("black", "pawn", False))
        self.game_service.board.set_piece((2, 7), ("black", "pawn", False))

        # White pieces
        self.game_service.board.set_piece((7, 7), ("white", "king", True))
        self.game_service.board.set_piece((3, 7), ("white", "bishop", False))
        self.game_service.board.set_piece((1, 3), ("white", "pawn", False))
        self.game_service.board.set_piece((3, 5), ("white", "pawn", False))
        self.game_service.board.set_piece((6, 1), ("white", "pawn", False))

        self.game_service.board.king_positions = {"white": (7, 7), "black": (1, 7)}

        ai_engine = AiEngine(7)

        # White should move bishop to check black
        ai_move = ai_engine.get_best_move(self.game_service.board)
        self.assertTrue(self.game_service.move_handler(ai_move))
        self.assertEqual(
            self.game_service.board.get_piece((5, 1)), ("white", "bishop", False)
        )

        # Black moves king away from check
        self.assertTrue(self.game_service.move_handler(((6, 0), (7, 1))))

        # White should checkmate through promotion
        ai_move2 = ai_engine.get_best_move(self.game_service.board)
        self.assertTrue(self.game_service.move_handler(ai_move2))
        self.assertEqual(
            self.game_service.board.get_piece((7, 4)), ("white", "queen", False)
        )
