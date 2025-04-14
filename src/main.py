import os
import sys
from entities.board import Board
from services.game_service import GameService
from services.ai_engine import AiEngine
from ui.game_window import GameWindow
from ui.main_menu import MainMenu


def main():
    platform_init()

    running = True
    while running:
        menu = MainMenu()
        config = menu.run()

        if config is None:
            sys.exit()

        if config["mode"] == "pvp":
            ai_engine = None
            board = Board("white")
        else:
            board = Board(config["player_color"])
            ai_engine = AiEngine(config["ai_depth"])

        game_service = GameService(board, ai_engine)
        game_window = GameWindow(game_service)

        continue_running = game_window.run()
        if not continue_running:
            running = False


def platform_init():
    if sys.platform.startswith("linux"):
        if not os.environ.get("XDG_RUNTIME_DIR"):
            directory = f"/tmp/runtime-{os.getpid()}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            os.environ["XDG_RUNTIME_DIR"] = directory


if __name__ == "__main__":
    main()
