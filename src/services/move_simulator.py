import copy
from entities.piece import Piece
from .move_validator import MoveValidator
from .board_evaluator import is_king_threatened


def process_move(board, validator_output, move):
    start_pos, end_pos = move
    match validator_output:
        case 0:
            # Illegal move
            return False
        case 2:
            # Pawn double step
            board.en_passant_target = [(7 - (end_pos[0] + 1), 7 - end_pos[1]), False]
        case 3:
            # En passant
            board.set_piece((start_pos[0], end_pos[1]), None)
        case 4:
            # Castle left
            board.set_piece((7, 3), board.get_piece((7, 0)))
            board.set_piece((7, 0), None)
        case 5:
            # Castle right
            board.set_piece((7, 5), board.get_piece((7, 7)))
            board.set_piece((7, 7), None)
    return True


def handle_en_passant_targeting(board):
    if board.en_passant_target:
        if board.en_passant_target[1]:
            board.en_passant_target = None
        else:
            board.en_passant_target[1] = True


def simulate_move(board, move):
    board = copy.deepcopy(board)

    handle_en_passant_targeting(board)

    validator_output = MoveValidator(board, move).validate_move()

    if not process_move(board, validator_output, move):
        return False

    start_pos, end_pos = move
    moved_piece = board.get_piece(start_pos)
    eaten_piece = board.get_piece(end_pos)

    board.stall_clock += 1

    if moved_piece.rank == "pawn":
        board.stall_clock = 0
        if end_pos[0] == 0:
            moved_piece = Piece(moved_piece.color, "queen")
    elif eaten_piece:
        board.stall_clock = 0

    board.set_piece(end_pos, moved_piece)
    board.set_piece(start_pos, None)

    if moved_piece.rank == "king":
        board.king_positions[board.player_color] = end_pos

    if is_king_threatened(board):
        return False

    return board
