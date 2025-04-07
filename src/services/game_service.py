import copy
from .move_simulator import simulate_move

class GameService:
    def __init__(self, board, ai_engine = None):
        self.board = board
        self.ai = ai_engine
        if board.player_color == "black":
            self.board.flip_board()
            if self.ai:
                ai_move = self.ai.get_best_move(copy.deepcopy(self.board))
                self.move_piece(ai_move)


    def move_handler(self, move):
        if not self.move_piece(move):
            return False
        
        if self.ai:
            ai_move = self.ai.get_best_move(copy.deepcopy(self.board))
            self.move_piece(ai_move)
        
        return self.board

    def move_piece(self, move):
        board = simulate_move(copy.deepcopy(self.board), move)

        if not board:
            return False
        
        board.flip_board()
        self.board = board
        
        return True
    

    def get_game_state():
        return 0
