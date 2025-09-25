PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 510,
    "queen": 975,
    "king": 0,
}


def evaluate_board(board):
    """Gets board material balance.

    Returns:
        Integer value of own pieces minus enemy pieces.
    """
    total = 0
    for row in board.board_matrix:
        for piece in row:
            if not piece:
                continue
            color, rank, _ = piece
            value = PIECE_VALUES[rank]
            if color == board.player_color:
                total += value
            else:
                total -= value
    return total
