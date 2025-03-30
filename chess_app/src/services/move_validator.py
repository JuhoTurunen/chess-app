class MoveValidator:
    def is_valid_move(self, board, start_pos, end_pos):
        moved_piece = board.get_piece_at(start_pos)
        if not moved_piece:
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
        y, x = start_pos
        ey, ex = end_pos
        print(y)
        print(ey)
        if ey == y - 1 and y - 1 >= 0:
            # Forward
            if x == ex and not board.get_piece_at(end_pos):
                return True

            print("a1")
            # Diagonal
            if (ex == x + 1 and x + 1 <= 7) or (ex == x - 1 and x - 1 >= 0):
                if board.get_piece_at(end_pos):
                    return True
                return False

        print("a2")
        return False
