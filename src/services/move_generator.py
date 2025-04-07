def generate_moves(board):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board.get_piece((row, col))
            if piece is not None and piece.color == board.player_color:
                match piece.type:
                    case "pawn":
                        moves.extend(generate_pawn_moves(row, col))
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
    return moves

def generate_pawn_moves(row, col):
    pawn_moves = []
    
    new_row = row - 1
    if 0 <= new_row:
        pawn_moves.append(((row, col), (new_row, col)))
        if 0 <= col - 1:
            pawn_moves.append(((row, col), (new_row, col - 1)))
        if col + 1 < 8:
            pawn_moves.append(((row, col), (new_row, col + 1)))
    if row == 6:
        pawn_moves.append(((row, col), (row - 2, col)))
    
    return pawn_moves
