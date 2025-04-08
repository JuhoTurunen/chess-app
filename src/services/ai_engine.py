import copy
from .move_generator import generate_moves
from .move_simulator import simulate_move
from .board_evaluator import evaluate_board


class AiEngine:
    def __init__(self, depth):
        self.depth = depth

    def get_best_move(self, board):
        board = copy.deepcopy(board)

        moves = generate_moves(board)
        if not moves:
            return None

        best_move = None
        best_score = -float("inf")

        for move in moves:

            new_board = simulate_move(board, move)
            if not new_board:
                continue

            new_board.flip_board()

            score = -self.negamax(new_board, self.depth - 1, -float("inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def negamax(self, board, depth, alpha, beta):
        if depth == 0:
            return evaluate_board(board)

        moves = generate_moves(board)
        if not moves:
            return evaluate_board(board)

        for move in moves:
            new_board = simulate_move(board, move)
            if not new_board:
                continue

            new_board.flip_board()

            score = -self.negamax(new_board, depth - 1, -beta, -alpha)

            alpha = max(alpha, score)

            if alpha >= beta:
                break

        return alpha
