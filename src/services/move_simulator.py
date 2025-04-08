import copy
from entities.piece import Piece
from .move_validator import MoveValidator


def simulate_move(board, move):
    start_pos, end_pos = move
    board = copy.deepcopy(board)

    if board.en_passant_target:
        if board.en_passant_target[1]:
            board.en_passant_target = None
        else:
            board.en_passant_target[1] = True

    result = MoveValidator().is_valid_move(board, start_pos, end_pos)
    match result:
        case 0:
            # Illegal Move
            return False
        case 2:
            # En passant
            board.set_piece((start_pos[0], end_pos[1]), None)
        case 3:
            # Castle left
            board.set_piece((7, 3), board.get_piece((7, 0)))
            board.set_piece((7, 0), None)
        case 4:
            # Castle right
            board.set_piece((7, 5), board.get_piece((7, 7)))
            board.set_piece((7, 7), None)

    moved_piece = board.get_piece(start_pos)

    if end_pos[0] == 0 and moved_piece.type == "pawn":
        moved_piece = Piece(moved_piece.color, "queen")

    board.set_piece(end_pos, moved_piece)
    board.set_piece(start_pos, None)

    return board
