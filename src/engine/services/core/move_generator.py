def generate_moves(board, only_active=False):
    """Generates all valid moves for current player.

    Args:
        board: Board object.
        only_active: If True, only return active moves

    Returns:
        List of move tuples (start, end) where each item is (row, col).
        Active moves are returned first.
    """
    active_moves = []
    quiet_moves = []

    for row in range(8):
        for col in range(8):
            piece = board.get_piece((row, col))
            if piece is not None and piece[0] == board.player_color:
                match piece[1]:
                    case "knight":
                        piece_active, piece_quiet = _generate_knight(row, col, board)
                    case "bishop":
                        piece_active, piece_quiet = _generate_bishop(row, col, board)
                    case "queen":
                        piece_active, piece_quiet = _generate_queen(row, col, board)
                    case "rook":
                        piece_active, piece_quiet = _generate_rook(row, col, board)
                    case "pawn":
                        piece_active, piece_quiet = _generate_pawn(row, col, board)
                    case "king":
                        piece_active, piece_quiet = _generate_king(row, col, board)

                active_moves.extend(piece_active)
                if not only_active:
                    quiet_moves.extend(piece_quiet)

    return active_moves if only_active else active_moves + quiet_moves


def _generate_pawn(row, col, board):
    active_moves = []
    quiet_moves = []

    new_row = row - 1
    if new_row < 0:
        return active_moves, quiet_moves

    # Peaceful moves
    target_piece = board.get_piece((new_row, col))
    if target_piece is None:
        if new_row == 0:
            # Promotion
            active_moves.append(((row, col), (new_row, col)))
        else:
            # Normal forward
            quiet_moves.append(((row, col), (new_row, col)))

        if row == 6:
            if board.get_piece((row - 2, col)) is None:
                # Double forward
                quiet_moves.append(((row, col), (row - 2, col)))

    # Attacking moves
    for col_offset in [-1, 1]:
        new_col = col + col_offset
        if not 0 <= new_col < 8:
            continue

        target_piece = board.get_piece((new_row, new_col))
        if target_piece is not None and target_piece[0] != board.player_color:
            # Diagonal capture
            active_moves.append(((row, col), (new_row, new_col)))
        elif (
            target_piece is None
            and board.en_passant_target
            and board.en_passant_target[0] == (new_row, new_col)
        ):
            # En passant
            active_moves.append(((row, col), (new_row, new_col)))

    return active_moves, quiet_moves


def _generate_knight(row, col, board):
    active_moves = []
    quiet_moves = []

    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for row_offset, col_offset in offsets:
        new_row = row + row_offset
        new_col = col + col_offset
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target_piece = board.get_piece((new_row, new_col))
            if target_piece is None:
                # Normal
                quiet_moves.append(((row, col), (new_row, new_col)))
            elif target_piece[0] != board.player_color:
                # Capture
                active_moves.append(((row, col), (new_row, new_col)))

    return active_moves, quiet_moves


def _generate_bishop(row, col, board):
    active_moves = []
    quiet_moves = []

    directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                break

            target_piece = board.get_piece((new_row, new_col))
            if target_piece is None:
                # Normal
                quiet_moves.append(((row, col), (new_row, new_col)))
            elif target_piece[0] != board.player_color:
                # Capture
                active_moves.append(((row, col), (new_row, new_col)))
                break
            else:
                # Blocked
                break

    return active_moves, quiet_moves


def _generate_rook(row, col, board):
    active_moves = []
    quiet_moves = []

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for row_direction, col_direction in directions:
        for i in range(1, 8):
            new_row = row + row_direction * i
            new_col = col + col_direction * i
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                break

            target_piece = board.get_piece((new_row, new_col))
            if target_piece is None:
                # Normal
                quiet_moves.append(((row, col), (new_row, new_col)))
            elif target_piece[0] != board.player_color:
                # Capture
                active_moves.append(((row, col), (new_row, new_col)))
                break
            else:
                # Blocked
                break

    return active_moves, quiet_moves


def _generate_queen(row, col, board):
    # Queen = bishop + rook
    bishop_active, bishop_quiet = _generate_bishop(row, col, board)
    rook_active, rook_quiet = _generate_rook(row, col, board)

    return bishop_active + rook_active, bishop_quiet + rook_quiet


def _generate_king(row, col, board):
    active_moves = []
    quiet_moves = []

    for row_direction in [-1, 0, 1]:
        for col_direction in [-1, 0, 1]:
            if row_direction == col_direction == 0:
                continue
            new_row = row + row_direction
            new_col = col + col_direction
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                continue

            target_piece = board.get_piece((new_row, new_col))
            if target_piece is None:
                # Normal
                quiet_moves.append(((row, col), (new_row, new_col)))
            elif target_piece[0] != board.player_color:
                # Capture
                active_moves.append(((row, col), (new_row, new_col)))

    if row == 7 and col == 4:
        # Castling
        king_piece = board.get_piece((row, col))
        if king_piece and not king_piece[2]:
            rook_right = board.get_piece((7, 7))
            if (
                rook_right
                and rook_right[1] == "rook"
                and not rook_right[2]
                and not board.get_piece((7, 5))
                and not board.get_piece((7, 6))
            ):
                quiet_moves.append(((row, col), (row, col + 2)))

            rook_left = board.get_piece((7, 0))
            if (
                rook_left
                and rook_left[1] == "rook"
                and not rook_left[2]
                and not board.get_piece((7, 1))
                and not board.get_piece((7, 2))
                and not board.get_piece((7, 3))
            ):
                quiet_moves.append(((row, col), (row, col - 2)))

    return active_moves, quiet_moves
