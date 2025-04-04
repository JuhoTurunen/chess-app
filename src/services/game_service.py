from entities.piece import Piece
from .move_validator import MoveValidator
import copy


class GameService:
    def __init__(self, board):
        self.board = board
        self.p1_turn = True
        if board.player_color == "black":
            self.p1_turn = False
            self.flip_board(self.board)
        self.score = [0, 0]
        self.mv = MoveValidator()

    def move_piece(self, start_pos, end_pos):
        board = copy.deepcopy(self.board)

        eaten_piece_pos = self.mv.is_valid_move(board, start_pos, end_pos)

        if eaten_piece_pos == False:
            return False

        moved_piece = board.get_piece(start_pos)

        if eaten_piece_pos:
            eaten_pece = board.get_piece(eaten_piece_pos)
            board.set_piece(eaten_piece_pos, None)
            if self.p1_turn:
                self.score[0] += eaten_pece.value
            else:
                self.score[1] += eaten_pece.value

        if moved_piece.type == "pawn" and end_pos[0] == 0:
            moved_piece = Piece(moved_piece.color, "queen")

        board.set_piece(end_pos, moved_piece)
        board.set_piece(start_pos, None)
    

        if not self.p1_turn:
            self.p1_turn = True
        else:
            self.p1_turn = False

        self.flip_board(board)
        self.board = board
        
        return self.board


    def flip_board(self, board):
        board.board_matrix = board.board_matrix[::-1, ::-1]
        board.player_color = "white" if board.player_color == "black" else "black"

    def get_game_state():
        return 0
