def evaluate_board(board):
    """Evaluates board material balance.

    Args:
        board: Board object.

    Returns:
        int
    """
    total = 0
    for row in board.board_matrix:
        for piece in row:
            if not piece:
                continue
            if piece.color == board.player_color:
                total += piece.value
            else:
                total -= piece.value
    return total


def is_king_threatened(board):
    """Checks if the current player's king is in check.

    Args:
        board: Board object.

    Returns:
        bool
    """
    k_row, k_col = board.king_positions[board.player_color]

    opponent_color = "white" if board.player_color == "black" else "black"

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

    for direction, piece_types in directions.items():
        if _check_direction(board, (k_row, k_col), direction, opponent_color, piece_types):
            return True

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
            if piece and piece.color == opponent_color and piece.rank == "knight":
                return True

    for row_direction, col_direction in [(-1, -1), (-1, 1)]:
        row, col = k_row + row_direction, k_col + col_direction
        if _is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if piece and piece.color == opponent_color and piece.rank == "pawn":
                return True

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


def _check_direction(board, start_pos, direction, opponent_color, attacking_types):
    """Scans a direction for attacking pieces.

    Args:
        board: Board object.
        start_pos: tuple
        direction: tuple
        opponent_color: str
        attacking_types: list

    Returns:
        bool
    """
    row, col = start_pos
    row_direction, col_direction = direction
    while True:
        row += row_direction
        col += col_direction
        if not _is_in_bounds(row, col):
            break
        piece = board.get_piece((row, col))
        if piece:
            if piece.color == opponent_color and piece.rank in attacking_types:
                return True
            break
    return False


def _is_in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8
