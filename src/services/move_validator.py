ILLEGAL_MOVE = 0
NORMAL_MOVE = 1
DOUBLE_STEP = 2
EN_PASSANT = 3
CASTLE_LEFT = 4
CASTLE_RIGHT = 5


class MoveValidator:
    def __init__(self, board, move):
        self.board = board
        self.start_pos, self.end_pos = move
        self.moved_piece = board.get_piece(self.start_pos)
        self.eaten_piece = board.get_piece(self.end_pos)

    def validate_move(self):
        if not self.moved_piece:
            return ILLEGAL_MOVE
        if not (0 <= self.end_pos[0] <= 7 and 0 <= self.end_pos[1] <= 7):
            return ILLEGAL_MOVE
        if self.board.player_color != self.moved_piece.color:
            return ILLEGAL_MOVE
        if self.eaten_piece and self.board.player_color == self.eaten_piece.color:
            return ILLEGAL_MOVE

        match self.moved_piece.rank:
            case "pawn":
                return self.validate_pawn_move()
            case "knight":
                return self.validate_knight_move()
            case "bishop":
                return self.validate_bishop_move()
            case "rook":
                return self.validate_rook_move()
            case "queen":
                return self.validate_queen_move()
            case "king":
                return self.validate_king_move()

    def validate_pawn_move(self):
        row, col = self.start_pos
        e_row, e_col = self.end_pos

        row_diff = row - e_row
        col_diff = abs(col - e_col)

        # Forward
        if row_diff == 1:
            if col_diff == 0 and not self.eaten_piece:
                return NORMAL_MOVE

            # Diagonal
            if col_diff == 1:
                if self.eaten_piece:
                    return NORMAL_MOVE

                # En passant
                if self.board.en_passant_target and self.board.en_passant_target[0] == (
                    e_row,
                    e_col,
                ):
                    return EN_PASSANT

        # Double forward
        elif row == 6 and e_row == 4 and col_diff == 0:
            first_step_row = e_row + 1
            if not self.board.get_piece((first_step_row, e_col)) and not self.eaten_piece:
                return DOUBLE_STEP

        return ILLEGAL_MOVE

    def validate_knight_move(self):
        row, col = self.start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return NORMAL_MOVE

        return ILLEGAL_MOVE

    def validate_bishop_move(self):
        row, col = self.start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if row_diff != col_diff:
            return ILLEGAL_MOVE

        row_step = 1 if e_row > row else -1
        col_step = 1 if e_col > col else -1

        c_row, c_col = row + row_step, col + col_step
        while (c_row, c_col) != (e_row, e_col):
            if self.board.get_piece((c_row, c_col)):
                return ILLEGAL_MOVE
            c_row += row_step
            c_col += col_step

        return NORMAL_MOVE

    def validate_rook_move(self):
        row, col = self.start_pos
        e_row, e_col = self.end_pos

        if row != e_row and col != e_col:
            return ILLEGAL_MOVE

        row_step = 0 if row == e_row else (1 if e_row > row else -1)
        col_step = 0 if col == e_col else (1 if e_col > col else -1)

        c_row, c_col = row + row_step, col + col_step
        while (c_row, c_col) != (e_row, e_col):
            if self.board.get_piece((c_row, c_col)):
                return ILLEGAL_MOVE
            c_row += row_step
            c_col += col_step

        self.moved_piece.has_moved = True

        return NORMAL_MOVE

    def validate_queen_move(self):
        rook_result = self.validate_rook_move()
        if rook_result:
            return rook_result

        bishop_result = self.validate_bishop_move()
        return bishop_result

    def validate_king_move(self):
        row, col = self.start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if row_diff <= 1 and col_diff <= 1:
            self.moved_piece.has_moved = True
            return NORMAL_MOVE

        # Castling
        if row == 7 and row_diff == 0 and col_diff == 2 and not self.moved_piece.has_moved:

            if e_col < col:
                rook_pos = (row, 0)
                path_positions = [(row, col - 1), (row, col - 2), (row, col - 3)]
            else:
                rook_pos = (row, 7)
                path_positions = [(row, col + 1), (row, col + 2)]

            rook = self.board.get_piece(rook_pos)
            if not rook or rook.rank != "rook" or rook.has_moved:
                return ILLEGAL_MOVE

            for pos in path_positions:
                if self.board.get_piece(pos):
                    return ILLEGAL_MOVE

            self.moved_piece.has_moved = True

            return CASTLE_LEFT if e_col < col else CASTLE_RIGHT

        return ILLEGAL_MOVE
