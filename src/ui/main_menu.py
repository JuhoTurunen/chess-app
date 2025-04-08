import pygame

WIDTH, HEIGHT = 640, 640
WHITE = (245, 245, 245)
BLACK = (50, 50, 50)
BUTTON_COLOR = (100, 150, 200)
HIGHLIGHT_COLOR = (150, 200, 250)
GROUP_BG = (230, 230, 230)
BORDER_COLOR = (200, 200, 200)


class Button:
    def __init__(self, label, width, height, data=None):
        self.label = label
        self.rect = pygame.Rect(0, 0, width, height)
        self.data = data

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, font, is_selected=False):
        color = HIGHLIGHT_COLOR if is_selected else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        label_surface = font.render(self.label, True, BLACK)
        label_rect = label_surface.get_rect(center=self.rect.center)
        screen.blit(label_surface, label_rect)


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.running = True

        self.selected_difficulty = 2
        self.selected_color = "white"

        # AI Game box
        self.ai_group_rect = pygame.Rect(WIDTH // 2 - 180, 170, 360, 260)

        # AI Game button
        self.start_ai_button = Button("Start AI Game", 280, 50)
        self.start_ai_button.rect.centerx = WIDTH // 2
        self.start_ai_button.rect.y = self.ai_group_rect.y + 20

        # Difficulty buttons
        self.difficulty_buttons = [
            Button("Easy", 100, 40, data=1),
            Button("Medium", 100, 40, data=2),
            Button("Hard", 100, 40, data=3),
        ]
        start_x = WIDTH // 2 - 155
        for i, btn in enumerate(self.difficulty_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self.start_ai_button.rect.bottom + 40

        # Color buttons
        self.color_buttons = [
            Button("White", 150, 40, data="white"),
            Button("Black", 150, 40, data="black"),
        ]
        start_x = WIDTH // 2 - 155
        for i, btn in enumerate(self.color_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self.difficulty_buttons[0].rect.bottom + 40

        # PVP button
        self.pvp_button = Button("Player vs Player", 280, 50)
        self.pvp_button.rect.centerx = WIDTH // 2
        self.pvp_button.rect.y = self.ai_group_rect.bottom + 30

        self.selected_config = None

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        return self.selected_config

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                for button in self.difficulty_buttons:
                    if button.is_clicked(pos):
                        self.selected_difficulty = button.data

                for button in self.color_buttons:
                    if button.is_clicked(pos):
                        self.selected_color = button.data

                if self.start_ai_button.is_clicked(pos):
                    self.selected_config = {
                        "mode": "ai",
                        "player_color": self.selected_color,
                        "ai_depth": self.selected_difficulty,
                    }
                    self.running = False

                if self.pvp_button.is_clicked(pos):
                    self.selected_config = {
                        "mode": "pvp",
                        "player_color": "white",
                        "ai_depth": None,
                    }
                    self.running = False

    def render(self):
        self.screen.fill(WHITE)

        # Title
        title = self.title_font.render("Chess App", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # AI settings box
        pygame.draw.rect(self.screen, GROUP_BG, self.ai_group_rect, border_radius=8)
        pygame.draw.rect(self.screen, BORDER_COLOR, self.ai_group_rect, width=2, border_radius=8)

        # Start AI Game button
        self.start_ai_button.draw(self.screen, self.font)

        # Difficulty buttons
        diff_label = self.font.render("Select Difficulty:", True, BLACK)
        diff_label_pos = (
            WIDTH // 2 - diff_label.get_width() // 2,
            self.start_ai_button.rect.bottom + 10,
        )
        self.screen.blit(diff_label, diff_label_pos)

        for button in self.difficulty_buttons:
            button.draw(self.screen, self.font, button.data == self.selected_difficulty)

        # Color buttons
        color_label = self.font.render("Select Color:", True, BLACK)
        color_label_pos = (
            WIDTH // 2 - color_label.get_width() // 2,
            self.difficulty_buttons[0].rect.bottom + 10,
        )
        self.screen.blit(color_label, color_label_pos)

        for button in self.color_buttons:
            button.draw(self.screen, self.font, button.data == self.selected_color)

        # PVP button
        self.pvp_button.draw(self.screen, self.font)

        pygame.display.flip()
