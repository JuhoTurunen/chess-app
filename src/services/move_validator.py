class MoveValidator:
    def is_valid_move(self, board, start_pos, end_pos):
        
        self.moved_piece = board.get_piece_at(start_pos)
        self.eaten_piece = board.get_piece_at(end_pos)
        
        if not self.moved_piece:
            return False
        if not (0 <= end_pos[0] <= 7 and 0 <= end_pos[1] <= 7):
            return False
        if board.player_color != self.moved_piece.color:
            return False
        if self.eaten_piece and board.player_color == self.eaten_piece.color:
            return False
        
        match self.moved_piece.type:
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
        row, col = start_pos
        e_row, e_col = end_pos
        if e_row == row - 1:
            # Forward
            if col == e_col and not self.eaten_piece:
                self.moved_piece.can_jump = False
                return None

            # Diagonal
            if (e_col == col + 1 or e_col == col - 1) and self.eaten_piece:
                self.moved_piece.can_jump = False
                return self.eaten_piece
        
        elif self.moved_piece.can_jump and e_row == row - 2:
            if col == e_col and not board.get_piece_at((e_col, e_row + 1)) and not board.get_piece_at(end_pos):
                self.moved_piece.can_jump = False
                return None
        
        return False

