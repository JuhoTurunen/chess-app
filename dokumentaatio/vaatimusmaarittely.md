# Requirements specification
## Purpose
Using the app, users can play chess against other players or in the future, an AI adversary.

## Core functionality
- The user can enter a game from the menu.
- The user can play chess against themselves or another player using the same computer.
  - The game engine will recognize victory and draw, ending the game in both cases.
- The user can end the game prematurely and return to the main menu.
- The user can exit the game from the main menu.

## Further development ideas
- User can change settings such as color scheme. These settings are saved.
- From the menu, the user can choose to play against an AI.
- The AI will have a rudimentary minimax algorithm and use alpha-beta pruning.
- The AI will use a database of the best starting moves to choose beginning moves.
- User can change AI difficulty when entering a game. This will change the depth of the minimax algorithm and whether the AI uses the database of best starting moves.
- User's win and loss counts against AI are stored on a scoreboard with separation based on AI difficulty.