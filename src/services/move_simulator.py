import copy
from entities.piece import Piece
from .move_validator import MoveValidator


def simulate_move(board, move):
    start_pos, end_pos = move
    board = copy.deepcopy(board)
    
    if board.en_passant_target and board.en_passant_target[1]:
        board.en_passant_target = None
    elif board.en_passant_target:
        board.en_passant_target[1] = True

    eaten_piece_pos = MoveValidator().is_valid_move(board, start_pos, end_pos)
    if eaten_piece_pos is False:
        return False

    moved_piece = board.get_piece(start_pos)

    if moved_piece.type == "king" and isinstance(eaten_piece_pos, str):
        if eaten_piece_pos == "right_castle":
            board.set_piece((7, 5), board.get_piece((7, 7)))
            board.set_piece((7, 7), None)
        elif eaten_piece_pos == "left_castle":
            board.set_piece((7, 3), board.get_piece((7, 0)))
            board.set_piece((7, 0), None)

    elif eaten_piece_pos:
        board.set_piece(eaten_piece_pos, None)

    if moved_piece.type == "pawn" and end_pos[0] == 0:
        moved_piece = Piece(moved_piece.color, "queen")

    board.set_piece(end_pos, moved_piece)
    board.set_piece(start_pos, None)

    return board
