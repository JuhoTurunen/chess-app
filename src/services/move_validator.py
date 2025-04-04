class MoveValidator:
    def is_valid_move(self, board, start_pos, end_pos):

        self.moved_piece = board.get_piece(start_pos)
        self.eaten_piece = board.get_piece(end_pos)

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
                return self.validate_pawn_move(board, start_pos, end_pos)
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

    def validate_pawn_move(self, board, start_pos, end_pos):
        row, col = start_pos
        e_row, e_col = end_pos
        if e_row == row - 1:
            # Forward
            if col == e_col and not self.eaten_piece:
                return None

            # Diagonal
            if e_col == col + 1 or e_col == col - 1:
                if self.eaten_piece:
                    return end_pos
                
                if row != 3:
                    return False
                
                en_passant_p = board.get_piece((row, e_col))
                if not en_passant_p or en_passant_p.type != "pawn":
                    return False

                if not en_passant_p.has_jumped or self.moved_piece.color == en_passant_p.color:
                    return False

                return (row, e_col)

        elif row == 6 and e_row == 4:
            if col == e_col and not board.get_piece((e_col, e_row + 1)) and not self.eaten_piece:
                self.moved_piece.has_jumped = True
                return None

        return False
