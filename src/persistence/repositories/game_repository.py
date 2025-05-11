from persistence.session import SessionLocal
from persistence.models.game import Game


class GameRepository:
    """Repository class for managing game records in the database."""

    def __init__(self):
        """Initializes a GameRepository with a new database session."""
        self._session = SessionLocal()

    def record_game(self, user_id, result, difficulty):
        """Saves a completed game to the database.

        Args:
            user_id: ID integer of the user.
            result: Game result (1 = win, 0 = draw, -1 = loss).
            difficulty: Game difficulty level (1 = easy, 2 = medium, 3 = hard).
        """
        game = Game(user_id=user_id, result=result, difficulty=difficulty)
        self._session.add(game)
        self._session.commit()
        self._session.refresh(game)

    def get_stats(self, user_id):
        """Retrieves win/draw/loss statistics by difficulty for a given user.

        Args:
            user_id: ID integer of the user.

        Returns:
            Stats summary per difficulty level (1-3).
        """
        stats_by_difficulty = {
            1: {"wins": 0, "draws": 0, "losses": 0},
            2: {"wins": 0, "draws": 0, "losses": 0},
            3: {"wins": 0, "draws": 0, "losses": 0},
        }

        games = self._session.query(Game).filter_by(user_id=user_id).all()
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
