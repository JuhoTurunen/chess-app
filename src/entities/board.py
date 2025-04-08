import numpy as np
from .piece import Piece as p


class Board:
    def __init__(self, p1_color):
        self.board_matrix = np.full((8, 8), None, dtype=object)
        self.player_color = p1_color
        self.en_passant_target = None
        self._setup_board(p1_color)

    def _setup_board(self, own_color):
        enemy_color = "white" if own_color == "black" else "black"

        if enemy_color == "black":
            enemy_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
            own_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        else:
            enemy_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]
            own_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]

        self.board_matrix[0] = [p(enemy_color, piece) for piece in enemy_pieces]
        self.board_matrix[7] = [p(own_color, piece) for piece in own_pieces]

        for i in range(8):
            self.board_matrix[1][i] = p(enemy_color, "pawn")
            self.board_matrix[6][i] = p(own_color, "pawn")

    def get_piece(self, position):
        row, col = position
        return self.board_matrix[row][col]

    def set_piece(self, position, piece):
        row, col = position
        self.board_matrix[row][col] = piece

    def flip_board(self):
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
