# Chess App

A chess application featuring a custom-built AI engine. Play against a friend locally or challenge the AI at three difficulty levels. User accounts track your win/loss record across sessions.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pygame](https://img.shields.io/badge/GUI-Pygame-green)
![Coverage](https://img.shields.io/badge/Coverage-90%25-brightgreen)

## Features

**Chess Engine**
- Complete chess rules implementation including castling, en passant, pawn promotion, and 50-move draw detection
- Board state represented as NumPy matrix with perspective flipping between turns

**AI Opponent**
- Negamax search with alpha-beta pruning
- Iterative deepening with time-limited search
- Transposition tables for position caching
- Quiescence search to prevent horizon effect
- Principal Variation Search (null window optimization)
- Piece-square tables with endgame-aware king positioning

**Application**
- Pygame GUI with piece highlighting and move validation
- Player vs Player and Player vs AI modes
- SQLite database for user accounts and game statistics

## Documentation

- [Architecture](./documentation/architecture.md) — System design, class diagrams, and AI algorithm details
- [Testing](./documentation/testing.md) — Test coverage and methodology
- [User Manual](./documentation/user_manual.md) — How to use the application

## Installation

**Prerequisites:** Python 3.10+, [Poetry](https://python-poetry.org/)

1. Clone the repository:
```bash
git clone https://github.com/JuhoTurunen/chess-app.git
cd chess-app
```

2. Install dependencies:
```bash
poetry install
```

3. Run the application:
```bash
poetry run invoke start
```

## Development

Run tests:
```bash
poetry run invoke test
```

Generate coverage report (output in `htmlcov/index.html`):
```bash
poetry run invoke coverage-report
```

Run linter:
```bash
poetry run invoke lint
```
