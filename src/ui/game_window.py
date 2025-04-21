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
    """Handles the GUI for the chess game.

    Attributes:
        game_service: Instance handling the chess game logic and state.
        board: game_service's board object.
        running: Controls the main loop execution.
        return_to_menu: Flag indicating if user wants to return to menu.
        screen: Pygame surface for rendering.
        clock: Pygame clock for framerate control.
        font: Font used for rendering most text.
        clicks: Stores board square selections (start and end positions).
        menu_button: Rect for menu button detection.
    """

    def __init__(self, game_service):
        """Initializes the window, rendering, and game control settings.

        Args:
            game_service: GameService instance.
        """
        self.game_service = game_service
        self.board = game_service.board
        self.running = True
        self.return_to_menu = False

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.clicks = []

        self.menu_button = pygame.Rect(10, 10, 70, 40)

    def run(self):
        """Main event/rendering loop.

        Returns:
            True if exiting to menu, else False
        """
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
            if self.return_to_menu:
                return True
        return False

    def handle_events(self):
        """Processes user interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                # Check for menu button click
                if self.menu_button.collidepoint(pos):
                    self.return_to_menu = True
                    self.running = False
                    return

                # Check for board click
                board_pos = self.get_board_square(pos)
                if board_pos:
                    if not self.clicks and not self.board.get_piece(board_pos):
                        return
                    self.clicks.append(board_pos)

                    if len(self.clicks) == 2:
                        new_board = self.game_service.move_handler(self.clicks)
                        if new_board:
                            self.board = new_board
                        self.clicks = []

    def get_board_square(self, mouse_pos):
        """Converts screen coordinates to board position.

        Args:
            mouse_pos: tuple mouse position in pixels.

        Returns:
            tuple (row, col) or None if out of bounds.
        """
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

    def render(self):
        """Renders the chess board, menu button, and end game overlay."""
        self.screen.fill(BG_COLOR)

        # Chess board
        for row in range(ROWS):
            for col in range(COLS):
                square_color = WHITE_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(
                    BOARD_OFFSET_X + col * SQUARE_SIZE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pygame.draw.rect(self.screen, square_color, rect)

                # Highlight
                if (row, col) in self.clicks:
                    square_highlight = WHITE_HIGHLIGHT if (row + col) % 2 == 0 else DARK_HIGHLIGHT
                    pygame.draw.rect(self.screen, square_highlight, rect)

                piece = self.board.get_piece((row, col))
                if piece:
                    image_path = f"assets/pieces/{piece.color}_{piece.rank}.png"
                    piece_image = pygame.image.load(image_path).convert_alpha()
                    image_rect = piece_image.get_rect(center=rect.center)
                    if piece.rank == "pawn" or piece.rank == "knight":
                        image_rect.x -= 1
                    self.screen.blit(piece_image, image_rect)

        pygame.draw.rect(self.screen, BUTTON_COLOR, self.menu_button, border_radius=5)
        menu_text = self.font.render("Menu", True, BLACK)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_rect)

        game_state = self.game_service.get_game_state()

        if game_state["game_over"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))

            message_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4)
            pygame.draw.rect(self.screen, WHITE, message_box, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, message_box, width=2, border_radius=10)

            winner = game_state["winner"]
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
            self.screen.blit(text, text_rect)

            continue_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 40)
            pygame.draw.rect(self.screen, BUTTON_COLOR, continue_button, border_radius=5)
            continue_text = self.font.render("Continue", True, BLACK)
            continue_rect = continue_text.get_rect(center=continue_button.center)
            self.screen.blit(continue_text, continue_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if continue_button.collidepoint(pos):
                    self.return_to_menu = True
                    self.running = False

        pygame.display.flip()
