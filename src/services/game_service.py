from .move_generator import generate_moves
from .move_simulator import simulate_move
from .board_evaluator import is_king_threatened


class GameService:
    def __init__(self, board, ai_engine=None):
        self.board = board
        self.ai = ai_engine
        if board.player_color == "black":
            self.board.flip_board()
            if self.ai:
                ai_move = self.ai.get_best_move(self.board)
                self.move_piece(ai_move)

    def move_handler(self, move):
        if not self.move_piece(move):
            return False

        if self.is_checkmate():
            print("Checkmate")
            return self.board

        if self.ai:
            ai_move = self.ai.get_best_move(self.board)
            if not self.move_piece(ai_move):
                print(f"AI move {ai_move} failed. \nBoard: \n{self.board}")

        if self.is_checkmate():
            print("Checkmate")

        return self.board

    def move_piece(self, move):
        board = simulate_move(self.board, move)

        if not board:
            return False

        board.flip_board()
        self.board = board

        return True

    def get_game_state(self):
        return 0

    def is_checkmate(self):
        if not is_king_threatened(self.board):
            return False

        moves = generate_moves(self.board)

        for move in moves:
            if not simulate_move(self.board, move):
                continue
            return False
        return True
