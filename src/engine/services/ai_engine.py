import hashlib
import time
from .core import simulate_move, generate_moves, is_in_check, evaluate_board


class AiEngine:
    """AI that selects best move using Negamax.

    Attributes:
        depth: Positive integer for minimum search depth.
        time_limit: Optional time limit in milliseconds.
    """

    CHECKMATE_SCORE = 100000
    INFINITY = 1000000

    def __init__(self, depth, time_limit=None):
        """Initializes AI with search depth and optional time limit.

        Args:
            depth: Positive integer for minimum search depth.
            time_limit: Optional time limit in milliseconds.
        """
        self.depth = depth
        self.time_limit = time_limit
        self._transposition_table = {}
        self._start_time = None
        self._current_depth = 0

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

        # Only let through moves where own king is not checked
        valid_moves = [move for move in moves if simulate_move(board, move)]

        if not valid_moves:
            return None

        if self.time_limit is not None:
            self._start_time = time.time()

        best_move = valid_moves[0]
        self._current_depth = 1

        while True:
            if self._current_depth > self.depth:
                if self.time_limit is None:
                    break
                elapsed_time = (time.time() - self._start_time) * 1000
                if elapsed_time >= self.time_limit:
                    break

            iteration_best_move = None
            alpha, beta = -self.INFINITY, self.INFINITY
            move_scores = []

            for move in valid_moves:
                if self._should_stop_search():
                    return best_move

                new_board = simulate_move(board, move)
                new_board.flip_board()

                score = -self._negamax(new_board, self._current_depth - 1, -beta, -alpha)

                if self._should_stop_search():
                    return best_move

                move_scores.append((score, move))

                if score > alpha:
                    alpha = score
                    iteration_best_move = move

                if alpha >= beta:
                    break

            best_move = iteration_best_move or best_move

            # Sort best scored moves first for better pruning in later iterations
            move_scores.sort(key=lambda x: x[0], reverse=True)
            valid_moves = [move for _, move in move_scores]

            self._current_depth += 1

        return best_move

    def _get_position_hash(self, board):
        """Generate a hash for the current board position.

        Returns:
            String hash representing the board position.
        """

        # Turn board position into a string
        def piece_to_string(piece):
            if piece is None:
                return "0"
            color, rank, has_moved = piece
            color_char = color[0]
            rank_char = rank[0] if rank != "knight" else "n"
            if rank in ("king", "rook"):
                return f"{color_char}{rank_char}{int(has_moved)}"
            return f"{color_char}{rank_char}"

        position_string = "".join(
            piece_to_string(piece) for row in board.board_matrix for piece in row
        )

        # Include player color and en passant information
        position_string += board.player_color[0]
        if board.en_passant_target:
            ep_pos, ep_flag = board.en_passant_target
            position_string += f"{ep_pos[0]}{ep_pos[1]}{int(ep_flag)}"

        return hashlib.md5(position_string.encode()).hexdigest()

    def _should_stop_search(self):
        """Check if search should stop due to time limit.

        Returns:
            Boolean indicating if search should stop.
        """
        if self.time_limit is None:
            return False

        if self._current_depth <= self.depth:
            return False

        elapsed_time = (time.time() - self._start_time) * 1000
        return elapsed_time >= self.time_limit

    def _negamax(self, board, depth, alpha, beta):
        """Negamax with alpha-beta pruning and a transposition table.

        Args:
            board: Board object.
            depth: Integer of remaining search depth.
            alpha: Integer of the best score for maximizing player.
            beta: Integer of the best score for minimizing player.

        Returns:
            Integer for best achievable material balance from given board state.
        """
        if self._should_stop_search():
            return 0

        original_alpha = alpha
        position_hash = self._get_position_hash(board)
        position_entry = self._transposition_table.get(position_hash)

        # Check transposition table
        if position_entry and position_entry["depth"] >= depth:
            if position_entry["value_type"] == "exact":
                return position_entry["score"]
            if position_entry["value_type"] == "lower_bound":
                alpha = max(alpha, position_entry["score"])
            elif position_entry["value_type"] == "upper_bound":
                beta = min(beta, position_entry["score"])

            if alpha >= beta:
                return position_entry["score"]

        moves = generate_moves(board)

        # Only let through moves where own king is not checked
        valid_moves = [
            (move, new_board) for move in moves if (new_board := simulate_move(board, move))
        ]

        # If no legal moves exist, player is checkmated or in stalemate
        if not valid_moves:
            return -self.CHECKMATE_SCORE + depth if is_in_check(board) else 0

        if depth == 0:
            return evaluate_board(board)

        # If position was evaluated previously, move the best known move to front for better pruning
        if position_entry and (best_known_move := position_entry["best_move"]):
            for i, (move, _) in enumerate(valid_moves):
                if move == best_known_move:
                    valid_moves.insert(0, valid_moves.pop(i))
                    break

        best_move = None
        search_interrupted = False

        for move, new_board in valid_moves:
            if self._should_stop_search():
                search_interrupted = True
                break

            new_board.flip_board()

            score = -self._negamax(new_board, depth - 1, -beta, -alpha)

            if self._should_stop_search():
                search_interrupted = True
                break

            if score > alpha:
                alpha = score
                best_move = move

            if alpha >= beta:
                break

        if not search_interrupted:
            value_type = "exact"
            if alpha <= original_alpha:
                value_type = "upper_bound"
            elif alpha >= beta:
                value_type = "lower_bound"

            self._transposition_table[position_hash] = {
                "score": alpha,
                "depth": depth,
                "value_type": value_type,
                "best_move": best_move,
            }

        return alpha
