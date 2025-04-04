import os
import sys
from entities.board import Board
from services.game_service import GameService
from ui.game_window import GameWindow

def main():
    if sys.platform.startswith("linux"):
        if not os.environ.get("XDG_RUNTIME_DIR"):
            dir = f"/tmp/runtime-{os.getuid()}"
            if not os.path.exists(dir):
                os.makedirs(dir)
            os.environ["XDG_RUNTIME_DIR"] = dir
            
    board = Board("white")
    game_service = GameService(board)
    game_window = GameWindow(game_service)
    game_window.run()

if __name__ == "__main__":
    main()