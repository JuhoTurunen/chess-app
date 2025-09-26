from .check_detector import is_in_check


def simulate_move(board, move):
    """Simulates a chess move, checking validity and updating state.

    Args:
        board: Board object.
        move: (start, end) positions as (row, col) tuples.

    Returns:
        Board object or False.
    """
    board = board.copy()

    _handle_en_passant_targeting(board)

    if not _process_special_moves(board, move):
        return False

    start_pos, end_pos = move
    moved_piece = board.get_piece(start_pos)
    eaten_piece = board.get_piece(end_pos)

    board.stall_clock += 1

    if moved_piece[1] == "pawn":
        board.stall_clock = 0
        if end_pos[0] == 0:
            moved_piece = (moved_piece[0], "queen", False)
    elif eaten_piece:
        board.stall_clock = 0

    if moved_piece[1] in ("king", "rook"):
        moved_piece = (moved_piece[0], moved_piece[1], True)

    board.set_piece(end_pos, moved_piece)
    board.set_piece(start_pos, None)

    if moved_piece[1] == "king":
        board.king_positions[board.player_color] = end_pos

    if is_in_check(board):
        return False

    return board


def _process_special_moves(board, move):
    """Processes special chess moves."""
    start_pos, end_pos = move
    moved_piece = board.get_piece(start_pos)

    if not moved_piece:
        return False

    piece_type = moved_piece[1]
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Pawn double step
    if (
        piece_type == "pawn"
        and start_row == 6
        and end_row == 4
        and start_col == end_col
    ):
        board.en_passant_target = [(7 - (end_row + 1), 7 - end_col), False]

    # En passant
    elif (
        piece_type == "pawn"
        and abs(start_col - end_col) == 1
        and not board.get_piece(end_pos)
        and board.en_passant_target
        and board.en_passant_target[0] == end_pos
    ):
        # Remove captured pawn
        board.set_piece((start_row, end_col), None)

    # Castling
    elif piece_type == "king" and abs(start_col - end_col) == 2:
        if end_col < start_col:
            # Left
            board.set_piece((7, 3), board.get_piece((7, 0)))
            board.set_piece((7, 0), None)
        else:
            # Right
            board.set_piece((7, 5), board.get_piece((7, 7)))
            board.set_piece((7, 7), None)

    return True


def _handle_en_passant_targeting(board):
    """Updates or clears en passant target on the board."""
    if board.en_passant_target:
        if board.en_passant_target[1]:
            board.en_passant_target = None
        else:
            board.en_passant_target[1] = True
