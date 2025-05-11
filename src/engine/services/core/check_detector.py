def is_in_check(board):
    """Checks if the current player's king is in check.

    Args:
        board: Board object.

    Returns:
        Boolean for whether own king is in check.
    """
    k_row, k_col = board.king_positions[board.player_color]

    if _attacked_by_sliders(board, k_row, k_col):
        return True
    if _attacked_by_knight(board, k_row, k_col):
        return True
    if _attacked_by_pawn(board, k_row, k_col):
        return True
    if _attacked_by_king(board, k_row, k_col):
        return True

    return False


def _attacked_by_sliders(board, k_row, k_col):
    """Checks if king is threatened by bishops, rooks, or queens."""
    directions = {
        (0, 1): ["rook", "queen"],
        (0, -1): ["rook", "queen"],
        (1, 0): ["rook", "queen"],
        (-1, 0): ["rook", "queen"],
        (1, 1): ["bishop", "queen"],
        (1, -1): ["bishop", "queen"],
        (-1, 1): ["bishop", "queen"],
        (-1, -1): ["bishop", "queen"],
    }

    for (row_direction, col_direction), piece_types in directions.items():
        row, col = k_row + row_direction, k_col + col_direction
        while _is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if not piece:
                row += row_direction
                col += col_direction
                continue
            if _not_own_piece(board, piece) and piece.rank in piece_types:
                return True
            break
    return False


def _attacked_by_knight(board, k_row, k_col):
    knight_positions = [
        (k_row - 2, k_col - 1),
        (k_row - 2, k_col + 1),
        (k_row - 1, k_col - 2),
        (k_row - 1, k_col + 2),
        (k_row + 1, k_col - 2),
        (k_row + 1, k_col + 2),
        (k_row + 2, k_col - 1),
        (k_row + 2, k_col + 1),
    ]

    for row, col in knight_positions:
        if _is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if _not_own_piece(board, piece) and piece.rank == "knight":
                return True
    return False


def _attacked_by_pawn(board, k_row, k_col):
    for row_direction, col_direction in [(-1, -1), (-1, 1)]:
        row, col = k_row + row_direction, k_col + col_direction
        if _is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if _not_own_piece(board, piece) and piece.rank == "pawn":
                return True
    return False


def _attacked_by_king(board, k_row, k_col):
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == col_offset == 0:
                continue

            row, col = k_row + row_offset, k_col + col_offset

            if not _is_in_bounds(row, col):
                continue

            piece = board.get_piece((row, col))
            if piece and piece.rank == "king":
                return True
    return False


def _not_own_piece(board, piece):
    return piece and piece.color != board.player_color


def _is_in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8
