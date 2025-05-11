import numpy as np
from .piece import Piece as p


class Board:
    """Represents the chess board and game state.

    Attributes:
        board_matrix: 8x8 matrix of Piece objects or None.
        player_color: Color whose perspective the board is oriented by.
        stall_clock: Number of moves without captures or pawn advances.
        en_passant_target: Optional tuple for en passant capture target.
        king_positions: Positions of both kings from the corresponding color's perspective.
    """

    def __init__(self, player_color: str):
        """Initializes board and piece positions.

        Args:
            player_color: Color ("white" or "black") of the player.
        """
        self.board_matrix = self._setup_board(player_color)
        self.player_color = player_color
        self.stall_clock = 0
        self.en_passant_target = None
        self.king_positions = {"white": (7, 4), "black": (7, 3)}

    def get_piece(self, position):
        """Gets the piece at a position.

        Args:
            position: (row, col) tuple for a board square.

        Returns:
            Piece or None, if no piece at location.
        """
        row, col = position
        return self.board_matrix[row][col]

    def set_piece(self, position, piece):
        """Sets a piece at a position.

        Args:
            position: (row, col) tuple for a board square.
            piece: Piece or None, if eaten piece's position is not replaced by another.
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
        """Gets board material balance.

        Returns:
            Integer value of own pieces minus enemy pieces.
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

    @staticmethod
    def _setup_board(player_color):
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
