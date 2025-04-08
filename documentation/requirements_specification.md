# Requirements specification
## Purpose
Using the app, users can play chess against other players or in the future, an AI adversary.

## Core functionality
- On startup, the user will land in the main menu.
- From the main menu, the user can select to play against themselves or an AI opponent.
  - The AI will use a minimax algorithm and alpha-beta pruning.
- The user can select to play as white or black.
- The user can enter a game of chess with their chosen settings.
  - The game engine will recognize victory, loss or draw, returning to the main menu in every case.
- The user can end the game prematurely and return to the main menu.
- The user can exit the game from the main menu.

## Further development ideas
- User can change settings such as color scheme. These settings are saved.
- The AI will use a database of the best starting moves to pick beginning moves.
- User can change AI difficulty when entering a game. This will change the depth of the minimax algorithm and whether the AI uses the database of best starting moves.
- User's wins and losses against the AI are stored on a scoreboard with separation based on AI difficulty and played color.
- After a game ends, the user can export a list of all the moves taken in the game.
