import os
import sys
from persistence.repositories.game_repository import GameRepository
from persistence.repositories.user_repository import UserRepository
from engine.entities.board import Board
from engine.services.game_service import GameService
from engine.services.ai_engine import AiEngine
from ui.game_window import GameWindow
from ui.main_menu import MainMenu


def main():
    platform_init()

    running = True
    user = None
    while running:
        menu = MainMenu(user, UserRepository(), GameRepository())
        config = menu.run()

        if config is None:
            sys.exit()

        if config["mode"] == "pvp":
            ai_engine = None
            board = Board("white")
        else:
            board = Board(config["player_color"])

            # Difficulty profiles
            match config["difficulty"]:
                case 1:
                    ai_engine = AiEngine(depth=2)
                case 2:
                    ai_engine = AiEngine(depth=3, time_limit=1000)
                case 3:
                    ai_engine = AiEngine(depth=3, time_limit=2500)
                case _:
                    ai_engine = AiEngine(depth=2)

        user = config["user"]
        game_service = GameService(board, ai_engine, user, GameRepository())
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
