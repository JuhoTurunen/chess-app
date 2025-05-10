import numpy as np
from .piece import Piece as p


class Board:
    """Represents the chess board and game state.

    Attributes:
        board_matrix: 8x8 numpy matrix of Piece objects or None.
        player_color: Color whose perspective the board is oriented by.
        en_passant_target: Optional tuple for en passant capture target.
        stall_clock: Number of moves without captures or pawn advances.
        king_positions: Positions of both kings from the corresponding color's perspective.
    """

    def __init__(self, player_color):
        """Initializes board and piece positions.

        Args:
            player_color: str
        """
        self.board_matrix = self._setup_board(player_color)
        self.player_color = player_color
        self.en_passant_target = None
        self.stall_clock = 0
        self.king_positions = {"white": (7, 4), "black": (7, 3)}

    def get_piece(self, position):
        """Gets the piece at a position.

        Args:
            position: tuple

        Returns:
            Piece or None
        """
        row, col = position
        return self.board_matrix[row][col]

    def set_piece(self, position, piece):
        """Sets a piece at a position.

        Args:
            position: tuple
            piece: Piece or None
        """
        row, col = position
        self.board_matrix[row][col] = piece

    def flip_board(self):
        """Flips board perspective."""
        self.board_matrix = self.board_matrix[::-1, ::-1]
        self.player_color = "white" if self.player_color == "black" else "black"

    def __repr__(self):
        board_str = ""
        for row in self.board_matrix:
            row_str = ""
            for piece in row:
                if not piece:
                    row_str += "-- "
                else:
                    row_str += f"{piece} "
            board_str += row_str + "\n"
        return board_str

    def material_balance(self):
        """Evaluates board material balance.

        Returns:
            int
        """
        total = 0
        for row in self.board_matrix:
            for piece in row:
                if not piece:
                    continue
                if piece.color == self.player_color:
                    total += piece.value
                else:
                    total -= piece.value
        return total

    def is_in_check(self):
        """Checks if the current player's king is in check.

        Returns:
            bool
        """
        k_row, k_col = self.king_positions[self.player_color]

        if self._attacked_by_sliders(k_row, k_col):
            return True
        if self._attacked_by_knight(k_row, k_col):
            return True
        if self._attacked_by_pawn(k_row, k_col):
            return True
        if self._attacked_by_king(k_row, k_col):
            return True

        return False

    def _attacked_by_sliders(self, k_row, k_col):
        """Checks if king is threatened by bishops, rooks, or queens."""
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

        for (row_direction, col_direction), piece_types in directions.items():
            row, col = k_row + row_direction, k_col + col_direction
            while self._is_in_bounds(row, col):
                piece = self.get_piece((row, col))
                if not piece:
                    row += row_direction
                    col += col_direction
                    continue
                if piece.color != self.player_color and piece.rank in piece_types:
                    return True
                break
        return False

    def _attacked_by_knight(self, k_row, k_col):
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
            if self._is_in_bounds(row, col):
                piece = self.get_piece((row, col))
                if piece and piece.color != self.player_color and piece.rank == "knight":
                    return True
        return False

    def _attacked_by_pawn(self, k_row, k_col):
        for row_direction, col_direction in [(-1, -1), (-1, 1)]:
            row, col = k_row + row_direction, k_col + col_direction
            if self._is_in_bounds(row, col):
                piece = self.get_piece((row, col))
                if piece and piece.color != self.player_color and piece.rank == "pawn":
                    return True
        return False

    def _attacked_by_king(self, k_row, k_col):
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == col_offset == 0:
                    continue

                row, col = k_row + row_offset, k_col + col_offset

                if not self._is_in_bounds(row, col):
                    continue

                piece = self.get_piece((row, col))
                if piece and piece.rank == "king":
                    return True
        return False

    @staticmethod
    def _is_in_bounds(row, col):
        return 0 <= row < 8 and 0 <= col < 8

    @staticmethod
    def _setup_board(player_color):
        """Sets up pieces on the board.

        Args:
            player_color: str

        Returns:
            np.ndarray
        """
        board_matrix = np.full((8, 8), None, dtype=object)
        enemy_color = "white" if player_color == "black" else "black"

        if enemy_color == "black":
            enemy_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
            own_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        else:
            enemy_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]
            own_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]

        board_matrix[0] = [p(enemy_color, piece) for piece in enemy_pieces]
        board_matrix[1] = [p(enemy_color, "pawn") for _ in range(8)]
        board_matrix[6] = [p(player_color, "pawn") for _ in range(8)]
        board_matrix[7] = [p(player_color, piece) for piece in own_pieces]

        return board_matrix
