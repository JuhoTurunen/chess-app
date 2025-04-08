def evaluate_board(board):
    total = 0
    for row in board.board_matrix:
        for piece in row:
            if not piece:
                continue
            if piece.color == board.player_color:
                total += piece.value
            else:
                total -= piece.value
    return total
