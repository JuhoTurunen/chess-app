# pylint: skip-file
import pygame
import re
from repositories.game_repository import GameRepository
from repositories.user_repository import UserRepository

WIDTH, HEIGHT = 800, 800
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
    def __init__(self, user=None):
        pygame.init()

        self.user = user
        self.username = ""
        self.game_repo = GameRepository()
        self.stats = self.game_repo.get_stats(self.user.id) if user else None

        self.username_error = ""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.running = True

        self.selected_difficulty = 2
        self.selected_color = "white"

        self.ai_group_rect = pygame.Rect(WIDTH // 2 - 180, 170, 360, 260)

        self.start_ai_button = Button("Start AI Game", 280, 50)
        self.start_ai_button.rect.centerx = WIDTH // 2
        self.start_ai_button.rect.y = self.ai_group_rect.y + 20

        self.difficulty_buttons = [
            Button("Easy", 100, 40, data=1),
            Button("Medium", 100, 40, data=2),
            Button("Hard", 100, 40, data=3),
        ]
        start_x = WIDTH // 2 - 155
        for i, btn in enumerate(self.difficulty_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self.start_ai_button.rect.bottom + 40

        self.color_buttons = [
            Button("White", 150, 40, data="white"),
            Button("Black", 150, 40, data="black"),
        ]
        start_x = WIDTH // 2 - 155
        for i, btn in enumerate(self.color_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self.difficulty_buttons[0].rect.bottom + 40

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

            if not self.user:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.is_valid_username(self.username):
                            self.init_user(self.username)
                            self.username_error = ""
                        else:
                            self.username_error = (
                                "Username must only use letters and numbers (1-50 characters)."
                            )
                    else:
                        self.username += event.unicode
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                        "user": self.user,
                    }
                    self.running = False

                if self.pvp_button.is_clicked(pos):
                    self.selected_config = {
                        "mode": "pvp",
                        "player_color": "white",
                        "ai_depth": None,
                        "user": None,
                    }
                    self.running = False

    def init_user(self, user):
        user_repo = UserRepository()
        self.user = user_repo.get_user(user) or user_repo.create_user(user)
        self.stats = self.game_repo.get_stats(self.user.id)

    def render(self):
        self.screen.fill(WHITE)

        title = self.title_font.render("Chess App", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        if self.user:
            self.render_game_start()
        else:
            prompt = self.font.render("Enter username:", True, BLACK)
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            self.screen.blit(prompt, prompt_rect)

            inp_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 40)
            pygame.draw.rect(self.screen, GROUP_BG, inp_box, border_radius=5)
            pygame.draw.rect(self.screen, BORDER_COLOR, inp_box, width=2, border_radius=5)

            text_surf = self.font.render(self.username, True, BLACK)
            self.screen.blit(text_surf, (inp_box.x + 10, inp_box.y + 8))

            if self.username_error:
                err = self.font.render(self.username_error, True, (200, 50, 50))
                err_rect = err.get_rect(center=(WIDTH // 2, inp_box.y + inp_box.height + 20))
                self.screen.blit(err, err_rect)

        pygame.display.flip()

    def render_game_start(self):
        pygame.draw.rect(self.screen, GROUP_BG, self.ai_group_rect, border_radius=8)
        pygame.draw.rect(self.screen, BORDER_COLOR, self.ai_group_rect, width=2, border_radius=8)

        self.start_ai_button.draw(self.screen, self.font)

        diff_label = self.font.render("Select Difficulty:", True, BLACK)
        diff_label_pos = (
            WIDTH // 2 - diff_label.get_width() // 2,
            self.start_ai_button.rect.bottom + 10,
        )
        self.screen.blit(diff_label, diff_label_pos)

        for button in self.difficulty_buttons:
            button.draw(self.screen, self.font, button.data == self.selected_difficulty)

        color_label = self.font.render("Select Color:", True, BLACK)
        color_label_pos = (
            WIDTH // 2 - color_label.get_width() // 2,
            self.difficulty_buttons[0].rect.bottom + 10,
        )
        self.screen.blit(color_label, color_label_pos)

        for button in self.color_buttons:
            button.draw(self.screen, self.font, button.data == self.selected_color)

        self.pvp_button.draw(self.screen, self.font)

        stats_y = self.pvp_button.rect.bottom + 40
        self.draw_stats(stats_y)

    def draw_stats(self, y_position):
        stats_box = pygame.Rect(WIDTH // 2 - 225, y_position + 30, 450, 150)
        pygame.draw.rect(self.screen, GROUP_BG, stats_box, border_radius=8)
        pygame.draw.rect(self.screen, BORDER_COLOR, stats_box, width=2, border_radius=8)

        stats_title = pygame.font.SysFont("Arial", 25).render(f"User {self.user.username} stats:", True, BLACK)
        self.screen.blit(stats_title, (stats_box.left + 40, stats_box.top + 25))

        labels_map = {1: "Easy", 2: "Medium", 3: "Hard"}

        for i, (diff, st) in enumerate(self.stats.items()):
            difficulty_label = self.font.render(labels_map.get(diff, diff), True, BLACK)
            diff_x = stats_box.left + 40 + i * 150
            self.screen.blit(difficulty_label, (diff_x, stats_box.top + 70))

            stats = f"{st['wins']}-{st['draws']}-{st['losses']}"
            record_surf = self.font.render(stats, True, BLACK)
            self.screen.blit(record_surf, (diff_x, stats_box.top + 100))

            wl_ratio = int(st["win_pct"])
            color = (50, 200, 50) if wl_ratio >= 50 else (200, 50, 50)
            pct_surf = self.font.render(f"{wl_ratio}%", True, color)
            self.screen.blit(pct_surf, (diff_x + 50, stats_box.top + 100))

    def is_valid_username(self, name):
        return 0 < len(name) <= 50 and re.fullmatch(r"[A-Za-z0-9]+", name) is not None
