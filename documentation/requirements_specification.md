# Requirements specification
## Purpose
The app allows users to play chess against other players or an AI adversary.

## Users
The application supports only one type of user. Login happens using only a username, and no password is required for authentication.

## Current features
### Navigation
- On startup, the user will land in a login/registration screen.
- On login/registration, the user is taken to a main menu where they can start the game.
- The user can end the game prematurely, returning to the main menu.
- The game engine detects victory, loss, or draw, returning to the main menu.

### Game
- Users can choose to play against themselves or an AI opponent.
- Against AI, users can select to play as white or black.
- Users can adjust AI difficulty before starting a game.
- The AI uses a minimax algorithm with alpha-beta pruning.

### Account
- Supports multiple users via username-only login on startup.
- The registration has basic username validation.
- The game tracks wins and losses against the AI on a scoreboard, categorized by AI difficulty.

## Planned features
- Implement a database of optimal opening moves for the AI to use in the early game.
- Allow users to export a list of all moves made after a game concludes.
- Implement user-specific customizable settings, such as color schemes, with preferences saved across sessions.
