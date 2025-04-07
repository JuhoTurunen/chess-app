import pygame

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (245, 245, 245)
BLACK = (50, 50, 50)


class GameWindow:
    def __init__(self, game_service):
        self.game_service = game_service
        self.board = game_service.board
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.clicks = []

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    def render(self):
        for row in range(ROWS):
            for col in range(COLS):
                square_color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, square_color, rect)

                piece = self.board.get_piece((row, col))
                if piece:
                    piece_color = WHITE if square_color == BLACK else BLACK
                    text_surface = self.font.render(piece.__repr__(), True, piece_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
