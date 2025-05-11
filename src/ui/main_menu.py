# pylint: skip-file
import pygame
import re

WIDTH, HEIGHT = 800, 800
WHITE = (245, 245, 245)
BLACK = (50, 50, 50)
BUTTON_COLOR = (100, 150, 200)
HIGHLIGHT_COLOR = (150, 200, 250)
GROUP_BG = (230, 230, 230)
BORDER_COLOR = (200, 200, 200)


class Button:
    """Represents a clickable button in the UI.

    Attributes:
        label: The text on the button.
        rect: Rectangle area for button placement.
        data: Optional data associated with the button.
    """

    def __init__(self, label, width, height, data=None):
        """Initializes the button.

        Args:
            label: str
            width: int
            height: int
            data: Optional
        """
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
    """Handles the main menu UI and user interaction."""

    def __init__(self, user=None, user_repository=None, game_repository=None):
        """Initializes the main menu.

        Args:
            user: Optional User object
        """

        self._user = user
        self._username = ""
        self._user_repo = user_repository
        self._game_repo = game_repository
        self._stats = self._game_repo.get_stats(self._user.id) if user else None
        self._running = True

        self._selected_difficulty = 2
        self._selected_color = "white"
        self._selected_config = None

        pygame.init()
        pygame.display.set_caption("Chess App")

        self._username_error = ""
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("Arial", 20)

        self._ai_group_rect = pygame.Rect(WIDTH // 2 - 180, 170, 360, 260)

        self._start_ai_button = Button("Start AI Game", 280, 50)
        self._start_ai_button.rect.centerx = WIDTH // 2
        self._start_ai_button.rect.y = self._ai_group_rect.y + 20

        self._pvp_button = Button("Player vs Player", 280, 50)
        self._pvp_button.rect.centerx = WIDTH // 2
        self._pvp_button.rect.y = self._ai_group_rect.bottom + 30

        self._difficulty_buttons = [
            Button("Easy", 100, 40, data=1),
            Button("Medium", 100, 40, data=2),
            Button("Hard", 100, 40, data=3),
        ]

        self._color_buttons = [
            Button("White", 150, 40, data="white"),
            Button("Black", 150, 40, data="black"),
        ]

        start_x = WIDTH // 2 - 155
        for i, btn in enumerate(self._difficulty_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self._start_ai_button.rect.bottom + 40

        for i, btn in enumerate(self._color_buttons):
            btn.rect.x = start_x + i * (btn.rect.width + 10)
            btn.rect.y = self._difficulty_buttons[0].rect.bottom + 40

    def run(self):
        """Main event/rendering loop.

        Returns:
            dict for selected game settings or None
        """
        while self._running:
            self._handle_events()
            self._render()
            self._clock.tick(60)
        return self._selected_config

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            if not self._user:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self._username = self._username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self._is_valid_username(self._username):
                            self._init_user(self._username)
                            self._username_error = ""
                        else:
                            self._username_error = (
                                "Username must only use letters and numbers (1-50 characters)."
                            )
                    else:
                        self._username += event.unicode
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                for button in self._difficulty_buttons:
                    if button.is_clicked(pos):
                        self._selected_difficulty = button.data

                for button in self._color_buttons:
                    if button.is_clicked(pos):
                        self._selected_color = button.data

                if self._start_ai_button.is_clicked(pos):
                    self._selected_config = {
                        "mode": "ai",
                        "player_color": self._selected_color,
                        "ai_depth": self._selected_difficulty,
                        "user": self._user,
                    }
                    self._running = False

                if self._pvp_button.is_clicked(pos):
                    self._selected_config = {
                        "mode": "pvp",
                        "player_color": "white",
                        "ai_depth": None,
                        "user": self._user,
                    }
                    self._running = False

    def _init_user(self, username):
        self._user = self._user_repo.get_user(username) or self._user_repo.create_user(username)
        self._stats = self._game_repo.get_stats(self._user.id)

    def _is_valid_username(self, name):
        return 0 < len(name) <= 50 and re.fullmatch(r"[A-Za-z0-9]+", name) is not None

    def _render(self):
        self._screen.fill(WHITE)

        title = pygame.font.SysFont("Arial", 48, bold=True).render("Chess App", True, BLACK)
        self._screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        if self._user:
            self._render_game_start()
        else:
            prompt = self._font.render("Enter username:", True, BLACK)
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            self._screen.blit(prompt, prompt_rect)

            inp_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 40)
            pygame.draw.rect(self._screen, GROUP_BG, inp_box, border_radius=5)
            pygame.draw.rect(self._screen, BORDER_COLOR, inp_box, width=2, border_radius=5)

            text_surf = self._font.render(self._username, True, BLACK)
            self._screen.blit(text_surf, (inp_box.x + 10, inp_box.y + 8))

            if self._username_error:
                err = self._font.render(self._username_error, True, (200, 50, 50))
                err_rect = err.get_rect(center=(WIDTH // 2, inp_box.y + inp_box.height + 20))
                self._screen.blit(err, err_rect)

        pygame.display.flip()

    def _render_game_start(self):
        pygame.draw.rect(self._screen, GROUP_BG, self._ai_group_rect, border_radius=8)
        pygame.draw.rect(self._screen, BORDER_COLOR, self._ai_group_rect, width=2, border_radius=8)

        self._start_ai_button.draw(self._screen, self._font)

        diff_label = self._font.render("Select Difficulty:", True, BLACK)
        diff_label_pos = (
            WIDTH // 2 - diff_label.get_width() // 2,
            self._start_ai_button.rect.bottom + 10,
        )
        self._screen.blit(diff_label, diff_label_pos)

        for button in self._difficulty_buttons:
            button.draw(self._screen, self._font, button.data == self._selected_difficulty)

        color_label = self._font.render("Select Color:", True, BLACK)
        color_label_pos = (
            WIDTH // 2 - color_label.get_width() // 2,
            self._difficulty_buttons[0].rect.bottom + 10,
        )
        self._screen.blit(color_label, color_label_pos)

        for button in self._color_buttons:
            button.draw(self._screen, self._font, button.data == self._selected_color)

        self._pvp_button.draw(self._screen, self._font)

        stats_y = self._pvp_button.rect.bottom + 40
        self._draw_stats(stats_y)

    def _draw_stats(self, y_position):
        stats_box = pygame.Rect(WIDTH // 2 - 225, y_position + 30, 450, 150)
        pygame.draw.rect(self._screen, GROUP_BG, stats_box, border_radius=8)
        pygame.draw.rect(self._screen, BORDER_COLOR, stats_box, width=2, border_radius=8)

        stats_title = pygame.font.SysFont("Arial", 25).render(
            f"Stats of {self._user.username}:", True, BLACK
        )
        self._screen.blit(stats_title, (stats_box.left + 40, stats_box.top + 25))

        labels_map = {1: "Easy", 2: "Medium", 3: "Hard"}

        for i, (diff, st) in enumerate(self._stats.items()):
            difficulty_label = self._font.render(labels_map.get(diff, diff), True, BLACK)
            diff_x = stats_box.left + 40 + i * 150
            self._screen.blit(difficulty_label, (diff_x, stats_box.top + 70))

            stats = f"{st['wins']}-{st['draws']}-{st['losses']}"
            record_surf = self._font.render(stats, True, BLACK)
            self._screen.blit(record_surf, (diff_x, stats_box.top + 100))

            wl_ratio = int(st["win_pct"])
            color = (50, 200, 50) if wl_ratio >= 50 else (200, 50, 50)
            pct_surf = self._font.render(f"{wl_ratio}%", True, color)
            self._screen.blit(pct_surf, (diff_x + 50, stats_box.top + 100))
