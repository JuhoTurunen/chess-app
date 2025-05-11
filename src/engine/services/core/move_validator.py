ILLEGAL_MOVE = 0
NORMAL_MOVE = 1
DOUBLE_STEP = 2
EN_PASSANT = 3
CASTLE_LEFT = 4
CASTLE_RIGHT = 5


class MoveValidator:
    """Validates a move based on board and piece rules."""

    def __init__(self, board, move):
        """Initializes with board and move.

        Args:
            board: Board object.
            move: (start, end) positions as (row, col) tuples.
        """
        self._board = board
        self._start_pos, self.end_pos = move
        self._moved_piece = board.get_piece(self._start_pos)
        self._eaten_piece = board.get_piece(self.end_pos)

    def validate_move(self):
        """Validates board move.

        Returns:
            Integer, where 0 is illegal, 1 is normal, and 2-5 are special moves.
        """
        illegal_conditions = [
            not self._moved_piece or self._board.player_color != self._moved_piece.color,
            not (0 <= self.end_pos[0] <= 7 and 0 <= self.end_pos[1] <= 7),
            self._eaten_piece and self._board.player_color == self._eaten_piece.color,
        ]

        if any(illegal_conditions):
            return ILLEGAL_MOVE

        rank_to_validator = {
            "pawn": self._validate_pawn_move,
            "knight": self._validate_knight_move,
            "bishop": self._validate_bishop_move,
            "rook": self._validate_rook_move,
            "queen": self._validate_queen_move,
            "king": self._validate_king_move,
        }

        validator = rank_to_validator.get(self._moved_piece.rank)
        return validator() if validator else ILLEGAL_MOVE

    def _validate_pawn_move(self):
        row, col = self._start_pos
        e_row, e_col = self.end_pos

        col_diff = abs(col - e_col)

        # Forward
        if row - e_row == 1:
            if col_diff == 0 and not self._eaten_piece:
                return NORMAL_MOVE

            # Diagonal
            if col_diff == 1:
                if self._eaten_piece:
                    return NORMAL_MOVE

                # En passant
                if self._board.en_passant_target and self._board.en_passant_target[0] == (
                    e_row,
                    e_col,
                ):
                    return EN_PASSANT

        # Double forward
        elif row == 6 and e_row == 4 and col_diff == 0:
            first_step_row = e_row + 1
            if not self._board.get_piece((first_step_row, e_col)) and not self._eaten_piece:
                return DOUBLE_STEP

        return ILLEGAL_MOVE

    def _validate_knight_move(self):
        row, col = self._start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return NORMAL_MOVE

        return ILLEGAL_MOVE

    def _validate_bishop_move(self):
        row, col = self._start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if row_diff != col_diff:
            return ILLEGAL_MOVE

        row_step = 1 if e_row > row else -1
        col_step = 1 if e_col > col else -1

        c_row, c_col = row + row_step, col + col_step
        while (c_row, c_col) != (e_row, e_col):
            if self._board.get_piece((c_row, c_col)):
                return ILLEGAL_MOVE
            c_row += row_step
            c_col += col_step

        return NORMAL_MOVE

    def _validate_rook_move(self):
        row, col = self._start_pos
        e_row, e_col = self.end_pos

        if row != e_row and col != e_col:
            return ILLEGAL_MOVE

        row_step = 0 if row == e_row else (1 if e_row > row else -1)
        col_step = 0 if col == e_col else (1 if e_col > col else -1)

        c_row, c_col = row + row_step, col + col_step
        while (c_row, c_col) != (e_row, e_col):
            if self._board.get_piece((c_row, c_col)):
                return ILLEGAL_MOVE
            c_row += row_step
            c_col += col_step

        self._moved_piece.has_moved = True

        return NORMAL_MOVE

    def _validate_queen_move(self):
        rook_result = self._validate_rook_move()
        if rook_result:
            return rook_result

        bishop_result = self._validate_bishop_move()
        return bishop_result

    def _validate_king_move(self):
        row, col = self._start_pos
        e_row, e_col = self.end_pos

        row_diff = abs(e_row - row)
        col_diff = abs(e_col - col)

        if row_diff <= 1 and col_diff <= 1:
            self._moved_piece.has_moved = True
            return NORMAL_MOVE

        # Castling
        if row == 7 and row_diff == 0 and col_diff == 2 and not self._moved_piece.has_moved:

            if e_col < col:
                rook_pos = (row, 0)
                path_positions = [(row, col - 1), (row, col - 2), (row, col - 3)]
            else:
                rook_pos = (row, 7)
                path_positions = [(row, col + 1), (row, col + 2)]

            rook = self._board.get_piece(rook_pos)
            if not rook or rook.rank != "rook" or rook.has_moved:
                return ILLEGAL_MOVE

            for pos in path_positions:
                if self._board.get_piece(pos):
                    return ILLEGAL_MOVE

            self._moved_piece.has_moved = True

            return CASTLE_LEFT if e_col < col else CASTLE_RIGHT

        return ILLEGAL_MOVE
