# Requirements specification
## Purpose
Using the app, users can play chess against other players or in the future, an AI adversary.

## Core functionality
- On startup, the user will land in the main menu. **(Done)**
- From the main menu, the user can select to play against themselves or an AI opponent. **(Done)**
  - The AI will use a minimax algorithm and alpha-beta pruning. **(Done)**
- The user can select to play as white or black. **(Done)**
- The user can enter a game of chess with their chosen settings. **(Done)**
- The game engine will recognize victory, loss, or draw, returning to the main menu in every case. **(Done)**
- The user can end the game prematurely, returning to the main menu. **(Done)**

## Further development ideas
- The app supports multiple users by username login on startup. **(Done)**
- User's wins and losses against the AI are stored on a scoreboard with separation based on AI difficulty and played color. **(Done)**
- User can change AI difficulty when entering a game. **(Done)**
- The AI will use a database of the best starting moves to pick beginning moves.
- After a game ends, the user can export a list of all the moves taken in the game.
- User can change settings such as color scheme. These settings are saved.
