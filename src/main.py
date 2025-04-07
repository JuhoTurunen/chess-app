import os
import sys
from entities.board import Board
from services.game_service import GameService
from services.ai_engine import AiEngine
from ui.game_window import GameWindow


def main():
    if sys.platform.startswith("linux"):
        if not os.environ.get("XDG_RUNTIME_DIR"):
            directory = f"/tmp/runtime-{os.getpid()}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            os.environ["XDG_RUNTIME_DIR"] = directory

    board = Board("white")
    ai_engine = AiEngine(3)
    game_service = GameService(board, ai_engine)
    game_window = GameWindow(game_service)
    game_window.run()


if __name__ == "__main__":
    main()
