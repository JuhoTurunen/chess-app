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
            if piece is not None and piece[0] == board.player_color:
                match piece[1]:
                    case "pawn":
                        moves.extend(_generate_pawn_moves(row, col, board))
                    case "knight":
                        moves.extend(_generate_knight_moves(row, col, board))
                    case "bishop":
                        moves.extend(_generate_bishop_moves(row, col, board))
                    case "rook":
                        moves.extend(_generate_rook_moves(row, col, board))
                    case "queen":
                        moves.extend(_generate_queen_moves(row, col, board))
                    case "king":
                        moves.extend(_generate_king_moves(row, col, board))
    return moves


def _generate_pawn_moves(row, col, board):
    pawn_moves = []

    new_row = row - 1
    if 0 <= new_row:
        target_piece = board.get_piece((new_row, col))
        if target_piece is None:
            pawn_moves.append(((row, col), (new_row, col)))
            if row == 6:
                double_move_piece = board.get_piece((row - 2, col))
                if double_move_piece is None:
                    pawn_moves.append(((row, col), (row - 2, col)))

        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_col < 8:
                target_piece = board.get_piece((new_row, new_col))
                if target_piece is not None and target_piece[0] != board.player_color:
                    pawn_moves.append(((row, col), (new_row, new_col)))
                elif (
                    target_piece is None
                    and board.en_passant_target
                    and board.en_passant_target[0] == (new_row, new_col)
                ):
                    pawn_moves.append(((row, col), (new_row, new_col)))

    return pawn_moves


def _generate_knight_moves(row, col, board):
    knight_moves = []

    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for row_offset, col_offset in offsets:
        new_row = row + row_offset
        new_col = col + col_offset
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target_piece = board.get_piece((new_row, new_col))
            if target_piece is None or target_piece[0] != board.player_color:
                knight_moves.append(((row, col), (new_row, new_col)))

    return knight_moves


def _generate_bishop_moves(row, col, board):
    bishop_moves = []

    directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece((new_row, new_col))
                if target_piece is None:
                    bishop_moves.append(((row, col), (new_row, new_col)))
                elif target_piece[0] != board.player_color:
                    bishop_moves.append(((row, col), (new_row, new_col)))
                    break
                else:
                    break
            else:
                break

    return bishop_moves


def _generate_rook_moves(row, col, board):
    rook_moves = []

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece((new_row, new_col))
                if target_piece is None:
                    rook_moves.append(((row, col), (new_row, new_col)))
                elif target_piece[0] != board.player_color:
                    rook_moves.append(((row, col), (new_row, new_col)))
                    break
                else:
                    break
            else:
                break

    return rook_moves


def _generate_queen_moves(row, col, board):
    queen_moves = _generate_bishop_moves(row, col, board) + _generate_rook_moves(
        row, col, board
    )
    return queen_moves


def _generate_king_moves(row, col, board):
    king_moves = []

    for row_direction in [-1, 0, 1]:
        for col_direction in [-1, 0, 1]:
            if row_direction == col_direction == 0:
                continue
            new_row = row + row_direction
            new_col = col + col_direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece((new_row, new_col))
                if target_piece is None or target_piece[0] != board.player_color:
                    king_moves.append(((row, col), (new_row, new_col)))

    if row == 7 and col == 4:
        king_moves.append(((row, col), (row, col + 2)))
        king_moves.append(((row, col), (row, col - 2)))

    return king_moves
