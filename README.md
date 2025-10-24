# Chess App

This application works as a chess engine. Using it, you can play chess against a friend on the same computer or against an AI opponent with varying difficulties. The game keeps score of your wins and losses against the AI opponent.

## Documentation
- [Specifications](https://github.com/JuhoTurunen/ot-harjoitustyo/blob/main/documentation/specifications.md)
- [Weekly reports](https://github.com/JuhoTurunen/ot-harjoitustyo/blob/main/documentation/weekly_reports/)
- [Testing](https://github.com/JuhoTurunen/ot-harjoitustyo/blob/main/documentation/testing.md)
- [Implementation](https://github.com/JuhoTurunen/ot-harjoitustyo/blob/main/documentation/implementation.md)
- [User manual](https://github.com/JuhoTurunen/ot-harjoitustyo/blob/main/documentation/user_manual.md)


## Installation

1. Clone the project with:

```bash
git clone https://github.com/JuhoTurunen/chess-app.git
```

2. After entering the project directory, install dependencies with:
   
```bash
poetry install
```

3. Start the app with:

```bash
poetry run invoke start
```

## Commands

You can start the chess app with:

```bash
poetry run invoke start
```

You can run tests with:

```bash
poetry run invoke test
```

You can generate a test coverage report (found in htmlcov/index.html) with:

```bash
poetry run invoke coverage-report
```

You can get a pylint command line report with:

```bash
poetry run invoke lint
```
