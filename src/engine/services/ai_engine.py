from .core import simulate_move, generate_moves, is_in_check, evaluate_board


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
        alpha = -1000000
        beta = 1000000

        for move in moves:
            new_board = simulate_move(board, move)
            if not new_board:
                continue

            new_board.flip_board()

            score = -self._negamax(new_board, self._depth - 1, -beta, -alpha)

            if score > alpha:
                alpha = score
                best_move = move

            if alpha >= beta:
                break

        return best_move

    def _negamax(self, board, depth, alpha, beta):
        """Negamax with alpha-beta pruning.

        Returns:
            Integer for best achievable material balance from given board state.
        """
        moves = generate_moves(board)

        valid_moves = []
        for move in moves:
            new_board = simulate_move(board, move)
            if new_board:
                valid_moves.append((move, new_board))

        if not valid_moves:
            if is_in_check(board):
                return -100000 + depth
            return 0

        if depth == 0:
            return evaluate_board(board)

        for move, new_board in valid_moves:
            new_board.flip_board()

            score = -self._negamax(new_board, depth - 1, -beta, -alpha)

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return alpha
