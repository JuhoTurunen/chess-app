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
    def __init__(self, game_service):
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
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
            if self.return_to_menu:
                return True
        return False

    def handle_events(self):
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
                    image_path = f"assets/pieces/{piece.color}_{piece.type}.png"
                    piece_image = pygame.image.load(image_path).convert_alpha()
                    image_rect = piece_image.get_rect(center=rect.center)
                    if piece.type == "pawn" or piece.type == "knight":
                        image_rect.x -= 1
                    self.screen.blit(piece_image, image_rect)

        # Menu button
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.menu_button, border_radius=5)
        menu_text = self.font.render("Menu", True, BLACK)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_rect)

        pygame.display.flip()
