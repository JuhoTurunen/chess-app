from .core import simulate_move, generate_moves, is_in_check

CHECKMATE = 1
DRAW = 2


class GameService:
    """Handles game flow, player/AI moves, and endgame logic.

    Attributes:
        board: Board object.
    """

    def __init__(self, board, ai_engine=None, user=None, game_repository=None):
        """Initializes GameService and calls the AI to do the first move, if it is white.

        Args:
            board: Board object.
            ai_engine: Optional AI engine object.
            user: Optional user object.
            game_repository: Optional GameRepository instance.
        """
        self.board = board
        self._ai = ai_engine
        self._winner = None
        self._user = user
        self._game_repo = game_repository

        if board.player_color == "black":
            self.board.flip_board()
            if self._ai:
                self._move_piece(self._ai.get_best_move(self.board))

    def get_winner(self):
        """Returns the winner of the game.

        Returns:
            String for winner or None if game is not over.
        """
        return self._winner

    def move_handler(self, move):
        """Processes a player move and the corresponding AI response, if present.

        Args:
            move: (start, end) positions as (row, col) tuples.

        Returns:
            Board object or False if the move was illegal.
        """
        if not self._move_piece(move):
            return False

        if end_state := self._is_game_over():
            self._game_end_handler(end_state)
            return self.board

        if self._ai:
            ai_move = self._ai.get_best_move(self.board)
            self._move_piece(ai_move)

            if end_state := self._is_game_over():
                self._game_end_handler(end_state, True)
                return self.board

        if self.board.stall_clock >= 50:
            self.board.flip_board()
            self._winner = "draw"

        return self.board

    def _move_piece(self, move):
        valid_moves = generate_moves(self.board)
        if move not in valid_moves:
            return False

        board = simulate_move(self.board, move)

        if not board:
            return False

        board.flip_board()
        self.board = board

        return True

    def _game_end_handler(self, end_state, ai_turn=False):
        result = None

        if end_state == CHECKMATE:
            if ai_turn:
                self._winner = "ai"
                result = -1
            else:
                self.board.flip_board()
                self._winner = "player" if self._ai else self.board.player_color
                result = 1
        elif end_state == DRAW:
            self._winner = "draw"
            if not ai_turn:
                self.board.flip_board()
            result = 0

        if self._user and self._ai:
            self._game_repo.record_game(self._user.id, result, self._ai.difficulty)

    def _is_game_over(self):
        moves = generate_moves(self.board)

        for move in moves:
            if not moves or not simulate_move(self.board, move):
                continue
            return False

        if is_in_check(self.board):
            return CHECKMATE
        return DRAW
