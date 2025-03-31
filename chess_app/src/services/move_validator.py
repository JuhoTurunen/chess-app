class MoveValidator:
    def is_valid_move(self, board, start_pos, end_pos):
        moved_piece = board.get_piece_at(start_pos)
        if not moved_piece:
            return False
        if not (0 <= end_pos[0] <= 7 and 0 <= end_pos[1] <= 7):
            return False
        
        match moved_piece.type:
            case "pawn":
                return self._validate_pawn_move(board, start_pos, end_pos)
            case "rook":
                pass
            case "knight":
                pass
            case "bishop":
                pass
            case "queen":
                pass
            case "king":
                pass

    def _validate_pawn_move(self, board, start_pos, end_pos):
        moved_piece = board.get_piece_at(start_pos)
        y, x = start_pos
        ey, ex = end_pos
        if ey == y - 1:
            # Forward
            if x == ex and not board.get_piece_at(end_pos):
                moved_piece.can_jump = False
                return True

            # Diagonal
            if ex == x + 1 or ex == x - 1:
                if board.get_piece_at(end_pos):
                    moved_piece.can_jump = False
                    return True
                return False
        elif moved_piece.can_jump and ey == y - 2:
            if x == ex and not board.get_piece_at((ex, ey + 1)) and not board.get_piece_at(end_pos):
                moved_piece.can_jump = False
                return True
        return False
