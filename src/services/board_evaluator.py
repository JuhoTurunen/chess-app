# Score
def evaluate_board(board):
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


# King check detection
def is_king_threatened(board):
    k_row, k_col = board.king_positions[board.player_color]

    opponent_color = "white" if board.player_color == "black" else "black"

    # Rook, bishop, and queen threats
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
        if check_direction(board, (k_row, k_col), direction, opponent_color, piece_types):
            return True

    # Knight threats
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
        if is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if piece and piece.color == opponent_color and piece.rank == "knight":
                return True

    # Pawn threats
    for row_direction, col_direction in [(-1, -1), (-1, 1)]:
        row, col = k_row + row_direction, k_col + col_direction
        if is_in_bounds(row, col):
            piece = board.get_piece((row, col))
            if piece and piece.color == opponent_color and piece.rank == "pawn":
                return True

    # King threats
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == col_offset == 0:
                continue

            row, col = k_row + row_offset, k_col + col_offset

            if not is_in_bounds(row, col):
                continue

            piece = board.get_piece((row, col))
            if piece and piece.rank == "king":
                return True

    return False


def check_direction(board, start_pos, direction, opponent_color, attacking_types):
    row, col = start_pos
    row_direction, col_direction = direction
    while True:
        row += row_direction
        col += col_direction
        if not is_in_bounds(row, col):
            break
        piece = board.get_piece((row, col))
        if piece:
            if piece.color == opponent_color and piece.rank in attacking_types:
                return True
            break
    return False


def is_in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8
