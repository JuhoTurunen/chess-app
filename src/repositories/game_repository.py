from services.db import SessionLocal
from entities.models import Game


class GameRepository:
    def __init__(self):
        self.session = SessionLocal()

    def record_game(self, user_id, result, difficulty):
        game = Game(user_id=user_id, result=result, difficulty=difficulty)
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def get_stats(self, user_id):
        stats_by_difficulty = {
            1: {"wins": 0, "draws": 0, "losses": 0},
            2: {"wins": 0, "draws": 0, "losses": 0},
            3: {"wins": 0, "draws": 0, "losses": 0},
        }

        games = self.session.query(Game).filter_by(user_id=user_id).all()
        for game in games:
            if game.result == 1:
                stats_by_difficulty[game.difficulty]["wins"] += 1
            elif game.result == 0:
                stats_by_difficulty[game.difficulty]["draws"] += 1
            elif game.result == -1:
                stats_by_difficulty[game.difficulty]["losses"] += 1

        stats_summary = {}
        for difficulty, record in stats_by_difficulty.items():
            total = record["wins"] + record["losses"] + record["draws"]
            win_pct = (record["wins"] / total * 100) if total else 0
            stats_summary[difficulty] = {**record, "win_pct": win_pct}

        return stats_summary
