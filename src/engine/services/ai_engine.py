import copy
from .move_generator import generate_moves
from .move_simulator import simulate_move


class AiEngine:
    """AI that selects best move using Negamax.

    Attributes:
        depth: int
    """

    def __init__(self, depth):
        """Initializes AI with search depth.

        Args:
            depth: int
        """
        self.depth = depth

    def get_best_move(self, board):
        """Finds best move for current player.

        Args:
            board: Board

        Returns:
            None or move tuple (start, end) where each item is (row, col)
        """
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

            score = -self._negamax(new_board, self.depth - 1, -float("inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _negamax(self, board, depth, alpha, beta):
        """Negamax with alpha-beta pruning.

        Args:
            board: Board
            depth: int
            alpha: float
            beta: float

        Returns:
            int
        """
        if depth == 0:
            return board.material_balance()

        moves = generate_moves(board)

        no_moves = True
        for move in moves:
            new_board = simulate_move(board, move)
            if not new_board:
                continue

            no_moves = False

            new_board.flip_board()

            score = -self._negamax(new_board, depth - 1, -beta, -alpha)

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        if no_moves:
            return -float("inf") if board.is_in_check() else 0

        return alpha
