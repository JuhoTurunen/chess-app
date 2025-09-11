from .core import simulate_move, generate_moves, is_in_check


class AiEngine:
    """AI that selects best move using Negamax.

    Attributes:
        difficulty: Positive integer for difficulty.
    """

    def __init__(self, difficulty):
        """Initializes AI with search depth.

        Args:
            difficulty: Positive integer for difficulty.
        """
        self.difficulty = difficulty
        self._depth = difficulty

    def get_best_move(self, board):
        """Finds best move for current player.

        Args:
            board: Board object.

        Returns:
            None or move tuple (start, end) where each item is (row, col).
        """
        board = board.copy()

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

            score = -self._negamax(new_board, self._depth - 1, -float("inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _negamax(self, board, depth, alpha, beta):
        """Negamax with alpha-beta pruning.

        Returns:
            Integer for best achievable material balance from given board state.
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
            return -float("inf") if is_in_check(board) else 0

        return alpha
