# User manual

## Installation and launch

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

## Use
### Registration and login
Once you have the app open, you'll land on a login screen. The app only requires a username to log in, and there is no separate registration screen. The username must only use numbers or letters and must be between 1 and 50 characters.

### Main menu
Inserting a valid username will take you to the main menu. Here you can start a game against an AI opponent or another player on the same computer. When playing against the AI you can set the AI's difficulty and whether you want to play as white or black. At the bottom of your screen, you will see your wins, draws, and losses (in that order) against each difficulty of AI.

### Game
Starting a game from the main menu will take you to a chess board. If you are playing against another player, the board will flip with each turn to indicate whose turn it is. When playing against AI, the AI will immediately respond to any moves you make. Draws will happen automatically and you won't be able to make any illegal moves. Selecting a piece will highlight it. You can return to the menu by pressing the "Menu" button at the top of the screen, but beware as this will delete your current game.

## Commands

As mentioned earlier, you can start the chess app with:

```bash
poetry run invoke start
```

In addition to that, you can also run tests with:

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