from repositories.game_repository import GameRepository
from .move_generator import generate_moves
from .move_simulator import simulate_move
from .board_evaluator import is_king_threatened


class GameService:
    """Handles game flow, player/AI moves, and endgame logic.

    Attributes:
        board: Board object.
        ai: AI engine or None.
        winner: Game end result.
        user: User object or None.
        game_repo: GameRepository instance if user is present.
    """

    def __init__(self, board, ai_engine=None, user=None):
        """Initializes GameService and calls the AI to do the first move, if it is white.

        Args:
            board: Board object.
            ai_engine: Optional AI engine object.
            user: Optional user object.
        """
        self.board = board
        self.ai = ai_engine
        self.winner = None
        if board.player_color == "black":
            self.board.flip_board()
            if self.ai:
                ai_move = self.ai.get_best_move(self.board)
                self._move_piece(ai_move)

        self.user = user
        if self.user:
            self.game_repo = GameRepository()

    def move_handler(self, move):
        """Processes a player move and the corresponding AI response, if present.

        Args:
            move: (start, end) positions as (row, col) tuples.

        Returns:
            Board object or False if the move was illegal
        """
        if not self._move_piece(move):
            return False

        end_state = self._is_game_over()
        if end_state:
            self._game_end_handler(end_state)
            return self.board

        if self.ai:
            ai_move = self.ai.get_best_move(self.board)
            self._move_piece(ai_move)

            end_state = self._is_game_over()
            if end_state:
                self._game_end_handler(end_state, True)
                return self.board

        if self.board.stall_clock >= 50:
            self.board.flip_board()
            self.winner = "draw"

        return self.board

    def get_game_state(self):
        """Returns the current game state.

        Returns:
            dict {"game_over": bool, "winner": str or None (if game is not over)}
        """
        if self.winner:
            return {"game_over": True, "winner": self.winner}
        return {"game_over": False, "winner": None}

    def _move_piece(self, move):
        """Attempts to apply a move to the board, and after, flips the board.

        Args:
            move: (start, end) positions as (row, col) tuples.

        Returns:
            bool (False if move was illegal, else True)
        """
        board = simulate_move(self.board, move)

        if not board:
            return False

        board.flip_board()
        self.board = board

        return True

    def _game_end_handler(self, end_state, ai_turn=False):
        """Handles different types of game end states.

        Args:
            end_state: int (1 for checkmate, 2 for draw)
            ai_turn: bool
        """
        result = None

        if end_state == 1:
            if ai_turn:
                self.winner = "ai"
                result = -1
            else:
                self.board.flip_board()
                self.winner = "player" if self.ai else self.board.player_color
                result = 1
        else:
            self.winner = "draw"
            if not ai_turn:
                self.board.flip_board()
            result = 0

        if self.user and self.ai:
            self.game_repo.record_game(self.user.id, result, self.ai.depth)

    def _is_game_over(self):
        """Identifies if game is over and how it ended.

        Returns:
            int (1 for checkmate, 2 for draw) or False if game has not ended
        """
        moves = generate_moves(self.board)

        for move in moves:
            if not simulate_move(self.board, move):
                continue
            return False

        if is_king_threatened(self.board):
            return 1
        return 2
