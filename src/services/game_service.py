from .move_generator import generate_moves
from .move_simulator import simulate_move
from .board_evaluator import is_king_threatened


class GameService:
    def __init__(self, board, ai_engine=None):
        self.board = board
        self.ai = ai_engine
        self.winner = None
        if board.player_color == "black":
            self.board.flip_board()
            if self.ai:
                ai_move = self.ai.get_best_move(self.board)
                self.move_piece(ai_move)

    def move_handler(self, move):
        if not self.move_piece(move):
            return False

        end_state = self.is_game_over()

        if end_state:
            self.board.flip_board()
            if end_state == 2:
                self.winner = "draw"
            elif self.ai:
                self.winner = "player"
            else:
                self.winner = self.board.player_color
            return self.board

        if self.ai:
            ai_move = self.ai.get_best_move(self.board)
            self.move_piece(ai_move)

            end_state = self.is_game_over()
            if end_state:
                self.winner = "ai" if end_state == 1 else "draw"

        if self.board.stall_clock >= 50:
            self.board.flip_board()
            self.winner = "draw"

        return self.board

    def move_piece(self, move):
        board = simulate_move(self.board, move)

        if not board:
            return False

        board.flip_board()
        self.board = board

        return True

    def is_game_over(self):
        moves = generate_moves(self.board)

        for move in moves:
            if not simulate_move(self.board, move):
                continue
            return False

        if is_king_threatened(self.board):
            return 1
        return 2

    def get_game_state(self):
        if self.winner:
            return {"game_over": True, "winner": self.winner}
        return {"game_over": False, "winner": None}
