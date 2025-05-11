def generate_moves(board):
    """Generates all pseudo-valid moves for current player.

    Args:
        board: Board object.

    Returns:
        List of move tuples (start, end) where each item is (row, col).
    """
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board.get_piece((row, col))
            if piece is not None and piece.color == board.player_color:
                match piece.rank:
                    case "pawn":
                        moves.extend(_generate_pawn_moves(row, col))
                    case "knight":
                        moves.extend(_generate_knight_moves(row, col))
                    case "bishop":
                        moves.extend(_generate_bishop_moves(row, col))
                    case "rook":
                        moves.extend(_generate_rook_moves(row, col))
                    case "queen":
                        moves.extend(_generate_queen_moves(row, col))
                    case "king":
                        moves.extend(_generate_king_moves(row, col))
    return moves


def _generate_pawn_moves(row, col):
    pawn_moves = []

    new_row = row - 1
    if 0 <= new_row:
        pawn_moves.append(((row, col), (new_row, col)))
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_col < 8:
                pawn_moves.append(((row, col), (new_row, new_col)))
        if row == 6:
            pawn_moves.append(((row, col), (row - 2, col)))

    return pawn_moves


def _generate_knight_moves(row, col):
    knight_moves = []

    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for row_offset, col_offset in offsets:
        new_row = row + row_offset
        new_col = col + col_offset
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            knight_moves.append(((row, col), (new_row, new_col)))

    return knight_moves


def _generate_bishop_moves(row, col):
    bishop_moves = []

    directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                bishop_moves.append(((row, col), (new_row, new_col)))
            else:
                break

    return bishop_moves


def _generate_rook_moves(row, col):
    rook_moves = []

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                rook_moves.append(((row, col), (new_row, new_col)))
            else:
                break

    return rook_moves


def _generate_queen_moves(row, col):
    queen_moves = _generate_bishop_moves(row, col) + _generate_rook_moves(row, col)
    return queen_moves


def _generate_king_moves(row, col):
    king_moves = []

    for row_direction in [-1, 0, 1]:
        for col_direction in [-1, 0, 1]:
            if row_direction == col_direction == 0:
                continue
            new_row = row + row_direction
            new_col = col + col_direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                king_moves.append(((row, col), (new_row, new_col)))

    if row == 7 and col == 4:
        king_moves.append(((row, col), (row, col + 2)))
        king_moves.append(((row, col), (row, col - 2)))

    return king_moves
