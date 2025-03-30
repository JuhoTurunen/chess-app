from .piece import Piece as p
import numpy as np


class Board:
    def __init__(self, playing_as):
        self.board_matrix = np.full((8, 8), None, dtype=object)
        self._setup_board(playing_as)

    def _setup_board(self, own_color):
        enemy_color = "black"
        if own_color == "black":
            enemy_color = "white"

        self.board_matrix[0][0] = p(enemy_color, "rook")
        self.board_matrix[0][7] = p(enemy_color, "rook")
        self.board_matrix[0][1] = p(enemy_color, "knight")
        self.board_matrix[0][6] = p(enemy_color, "knight")
        self.board_matrix[0][2] = p(enemy_color, "bishop")
        self.board_matrix[0][5] = p(enemy_color, "bishop")

        self.board_matrix[7][0] = p(own_color, "rook")
        self.board_matrix[7][7] = p(own_color, "rook")
        self.board_matrix[7][1] = p(own_color, "knight")
        self.board_matrix[7][6] = p(own_color, "knight")
        self.board_matrix[7][2] = p(own_color, "bishop")
        self.board_matrix[7][5] = p(own_color, "bishop")

        if enemy_color == "black":
            self.board_matrix[0][3] = p(enemy_color, "queen")
            self.board_matrix[0][4] = p(enemy_color, "king")
            self.board_matrix[7][3] = p(own_color, "queen")
            self.board_matrix[7][4] = p(own_color, "king")
        else:
            self.board_matrix[0][3] = p(enemy_color, "king")
            self.board_matrix[0][4] = p(enemy_color, "queen")
            self.board_matrix[7][3] = p(own_color, "king")
            self.board_matrix[7][4] = p(own_color, "queen")

        for i in range(8):
            self.board_matrix[1][i] = p(enemy_color, "pawn")
            self.board_matrix[6][i] = p(own_color, "pawn")

    def get_piece_at(self, position):
        row, col = position
        return self.board_matrix[row][col]

    def set_piece_at(self, position, piece):
        row, col = position
        self.board_matrix[row][col] = piece

    def __repr__(self):
        piece_symbols = {
            "pawn": "P",
            "rook": "R",
            "knight": "N",
            "bishop": "B",
            "queen": "Q",
            "king": "K",
        }
        board_str = ""
        for row in self.board_matrix:
            row_str = ""
            for piece in row:
                if piece is None:
                    row_str += "-- "
                else:
                    row_str += f"{piece.color[0]}{piece_symbols[piece.type]} "
            board_str += row_str.rstrip() + "\n"
        return board_str.rstrip()
