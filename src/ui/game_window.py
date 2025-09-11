# pylint: skip-file
import pygame

BOARD_SIZE = 640
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2

WHITE = (245, 245, 245)
BLACK = (50, 50, 50)
WHITE_SQUARE = (235, 235, 210)
DARK_SQUARE = (115, 150, 80)
WHITE_HIGHLIGHT = (245, 245, 130)
DARK_HIGHLIGHT = (185, 202, 65)
BUTTON_COLOR = (100, 150, 200)
BG_COLOR = (220, 220, 220)


class GameWindow:
    """Handles the GUI for the chess game."""

    def __init__(self, game_service):
        """Initializes the window, rendering, and game control settings.

        Args:
            game_service: GameService instance.
        """
        self._game_service = game_service
        self._board = game_service.board
        self._running = True
        self._return_to_menu = False

        pygame.init()
        pygame.display.set_caption("Chess App")

        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("Arial", 24)
        self._clicks = []

        self._menu_button = pygame.Rect(10, 10, 70, 40)

    def run(self):
        """Main event/rendering loop.

        Returns:
            True if returning to menu, else False, if closing program.
        """
        while self._running:
            self._handle_events()
            self._render()
            self._clock.tick(60)
            if self._return_to_menu:
                return True
        return False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                # Check for menu button click
                if self._menu_button.collidepoint(pos):
                    self._return_to_menu = True
                    self._running = False
                    return

                # Check for board click
                board_pos = self._get_board_square(pos)
                if board_pos:
                    if not self._clicks and not self._board.get_piece(board_pos):
                        return
                    self._clicks.append(board_pos)

                    if len(self._clicks) == 2:
                        new_board = self._game_service.move_handler(self._clicks)
                        if new_board:
                            self._board = new_board
                        self._clicks = []

    def _get_board_square(self, mouse_pos):
        x, y = mouse_pos

        if (
            x < BOARD_OFFSET_X
            or x >= BOARD_OFFSET_X + BOARD_SIZE
            or y < BOARD_OFFSET_Y
            or y >= BOARD_OFFSET_Y + BOARD_SIZE
        ):
            return None

        board_x = x - BOARD_OFFSET_X
        board_y = y - BOARD_OFFSET_Y

        col = board_x // SQUARE_SIZE
        row = board_y // SQUARE_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    def _render(self):
        self._screen.fill(BG_COLOR)

        self._render_board()

        pygame.draw.rect(self._screen, BUTTON_COLOR, self._menu_button, border_radius=5)
        menu_text = self._font.render("Menu", True, BLACK)
        menu_rect = menu_text.get_rect(center=self._menu_button.center)
        self._screen.blit(menu_text, menu_rect)

        if winner := self._game_service.get_winner():
            self._render_game_over(winner)

        pygame.display.flip()

    def _render_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                square_color = WHITE_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(
                    BOARD_OFFSET_X + col * SQUARE_SIZE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pygame.draw.rect(self._screen, square_color, rect)

                # Highlight
                if (row, col) in self._clicks:
                    square_highlight = WHITE_HIGHLIGHT if (row + col) % 2 == 0 else DARK_HIGHLIGHT
                    pygame.draw.rect(self._screen, square_highlight, rect)

                piece = self._board.get_piece((row, col))
                if piece:
                    image_path = f"assets/pieces/{piece[0]}_{piece[1]}.png"
                    piece_image = pygame.image.load(image_path).convert_alpha()
                    image_rect = piece_image.get_rect(center=rect.center)
                    if piece[1] == "pawn" or piece[1] == "knight":
                        image_rect.x -= 1
                    self._screen.blit(piece_image, image_rect)

    def _render_game_over(self, winner):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self._screen.blit(overlay, (0, 0))

        message_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4)
        pygame.draw.rect(self._screen, WHITE, message_box, border_radius=10)
        pygame.draw.rect(self._screen, BLACK, message_box, width=2, border_radius=10)

        message = ""
        match winner:
            case "ai":
                message = "You lost!"
            case "player":
                message = "You won!"
            case "draw":
                message = "Draw!"
            case _:
                message = f"{winner.capitalize()} wins!"

        text = pygame.font.SysFont("Arial", 48, bold=True).render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 48))
        self._screen.blit(text, text_rect)

        continue_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 40)
        pygame.draw.rect(self._screen, BUTTON_COLOR, continue_button, border_radius=5)
        continue_text = self._font.render("Continue", True, BLACK)
        continue_rect = continue_text.get_rect(center=continue_button.center)
        self._screen.blit(continue_text, continue_rect)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if continue_button.collidepoint(pos):
                self._return_to_menu = True
                self._running = False
