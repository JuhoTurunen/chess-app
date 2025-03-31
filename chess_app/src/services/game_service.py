from .move_validator import MoveValidator


class GameService:
    def __init__(self, board):
        self.board = board
        self.p1_turn = True if board.p1_color == "white" else False
        self.score = [0, 0]
        self.mv = MoveValidator()

    def move_piece(self, start_pos, end_pos):
        board = self.board

        if not self.p1_turn:
            board = self.get_flipped_board()

        result = self.mv.is_valid_move(board, start_pos, end_pos)

        if not result:
            return False

        moved_piece = board.get_piece_at(start_pos)

        if (board.p1_color != moved_piece.color and self.p1_turn) or (
            board.p1_color == moved_piece.color and not self.p1_turn
        ):
            return False

        eaten_piece = board.get_piece_at(end_pos)

        if eaten_piece:
            if eaten_piece.color == moved_piece.color:
                return False

            if self.p1_turn:
                self.score[0] += 1
            else:
                self.score[1] += 1

        board.set_piece_at(end_pos, moved_piece)
        board.set_piece_at(start_pos, None)

        if not self.p1_turn:
            board = self.get_flipped_board()
            self.p1_turn = True
        else:
            self.p1_turn = False

        self.board = board

        return self.board

    def get_flipped_board(self):
        flipped = self.board
        flipped.board_matrix = flipped.board_matrix[::-1, ::-1]
        return flipped

    def get_game_state():
        return 0
