PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 510,
    "queen": 975,
    "king": 0,
}

POSITION_VALUES = {
    "pawn": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 35, 35, 20, 10, 10],
        [5, 5, 10, 30, 30, 10, 5, 5],
        [0, 0, 0, 25, 25, 0, 0, 0],
        [5, -5, -10, 5, 5, -10, -5, 5],
        [5, 10, 10, -25, -25, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "knight": [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 25, 25, 15, 5, -30],
        [-30, 0, 15, 25, 25, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    "bishop": [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 12, 12, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    "rook": [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [35, 40, 40, 40, 40, 40, 40, 35],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "queen": [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    "king": [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ],
    "king_endgame": [
        [-20, -30, -30, -30, -30, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 10, 20, 20, 10, 5, 5],
        [5, 5, 10, 20, 20, 10, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
}


def evaluate_board(board):
    """Gets board material balance and positional value.

    Returns:
        Integer value of own pieces minus enemy pieces, including positional bonuses.
    """
    total_material = 0
    total = 0
    kings = []

    for row_index, row in enumerate(board.board_matrix):
        for col_index, piece in enumerate(row):
            if not piece:
                continue
            color, rank, _ = piece

            piece_value = PIECE_VALUES[rank]
            total_material += piece_value

            eval_row = row_index
            eval_col = col_index

            if color != board.player_color:
                eval_row = 7 - eval_row

            if color == "black":
                eval_col = 7 - eval_col

            if rank == "king":
                kings.append((eval_row, eval_col, color))
                continue

            positional_bonus = POSITION_VALUES[rank][eval_row][eval_col]
            total_piece_value = piece_value + positional_bonus

            if color == board.player_color:
                total += total_piece_value
            else:
                total -= total_piece_value

    is_endgame = total_material < 2200

    # Evaluate kings with different tables based on gamestage
    for eval_row, eval_col, color in kings:
        king_table = "king_endgame" if is_endgame else "king"
        positional_bonus = POSITION_VALUES[king_table][eval_row][eval_col]

        if color == board.player_color:
            total += positional_bonus
        else:
            total -= positional_bonus

    return total
