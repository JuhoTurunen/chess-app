from entities.piece import Piece
from .move_validator import MoveValidator

def simulate_move(board, move):
        start_pos, end_pos = move
        
        eaten_piece_pos = MoveValidator().is_valid_move(board, start_pos, end_pos)
        if eaten_piece_pos == False:
            return False

        moved_piece = board.get_piece(start_pos)

        if eaten_piece_pos:
            board.set_piece(eaten_piece_pos, None)

        if moved_piece.type == "pawn" and end_pos[0] == 0:
            moved_piece = Piece(moved_piece.color, "queen")

        board.set_piece(end_pos, moved_piece)
        board.set_piece(start_pos, None)

        return board