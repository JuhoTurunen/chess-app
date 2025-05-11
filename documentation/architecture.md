# Architecture

## High-level description
The architecture is mainly divided into three main components:
- UI
- Engine
  - Entities
  - Services
- Persistence
  - Models
  - Repositories


The main.py file serves as the entry point for the program as well as a coordinator of the three different components. It initiates MainMenu and passes the game setting info it receives from there to the GameService. The GameService itself is passed to the UI level's GameWindow. From there on, the window sends board moves to the GameService, which returns a board to the GameWindow for rendering. 

Within the Engine, the GameService is central. It manages the game state, which is represented by Entities like the Board and Piece objects. When processing moves, GameService utilizes other Services within the Engine, such as the AIEngine (if playing against an AI) and the core chess logic functions (for validating moves, simulating them, detecting checks, and generating possible moves). These core functions operate directly on the Board entity.

The Persistence layer handles saving and loading data. The MainMenu uses Repositories (UserRepository and GameRepository) to fetch user information and display statistics, or to create new users. Similarly, after a game concludes, the GameService can use a GameRepository to record the game's outcome. 

### Program arcitechture
Here is a highly abstracted class diagram for the entire chess engine:
```mermaid
classDiagram
    %% UI Layer
    class MainMenu {
      +run()
      -_user : User
      -_user_repo : UserRepository
      -_game_repo : GameRepository
      +handle_events()
      +render()
    }
    class GameWindow {
      +run()
      -_game_service : GameService
      +handle_events()
      +render()
    }

    %% Engine Layer - Services
    class GameService {
      +board : Board
      -_ai : AiEngine
      -_user : User
      -_game_repo : GameRepository
      +move_handler(move)
      +get_winner()
    }
    class AiEngine {
      +get_best_move(board: Board)
    }

    %% Engine Layer - Entities
    class Board {
      +board_matrix
      +player_color
      +get_piece(position)
      +set_piece(position, piece)
      +flip_board()
    }
    class Piece {
      <<entity>>
      +color
      +rank
      +value
    }

    %% Persistence Layer - Repositories
    class UserRepository {
      +get_user(username) User
      +create_user(username) User
    }
    class GameRepository {
      +get_stats(user_id)
      +record_game(user_id, result, difficulty)
    }

    %% Persistence Layer - Models/Entities
    class User {
      <<entity>>
      +id
      +username
    }

    %% Relationships
    MainMenu --> GameService : provides config for
    MainMenu --> UserRepository : uses
    MainMenu --> GameRepository : uses for stats

    GameWindow --> GameService : uses

    GameService "1" *-- "1" Board : manages
    GameService o-- "0..1" AiEngine : optional dependency
    GameService --> GameRepository : records game with
    GameService --> User : associated with

    AiEngine --> Board : analyzes

    Board "1" *-- "0..*" Piece : contains

    UserRepository ..> User : creates/retrieves

```
## Turn sequence diagram
Here is a high-level sequence diagram for the actions taken after a player selects a move in the game window (and when the player's color is white). The player's color and whether they play against AI or another player is dictated by the config received from the main menu. The "AI Move" branch only triggers if the player is playing against AI.
```mermaid
sequenceDiagram
    participant GW as GameWindow
    participant GS as GameService
    participant A as AiEngine
    participant S as simulate_move

    GW->>GW: render()
    Note over GW: User selects a move
    GW->>+GS: move_handler([first_click, second_click])
    
    GS->>+S: simulate_move(board, player_move)
    S-->>-GS: new_board
    GS->>GS: new_board.flip_board()
    GS->>GS: Update self.board with new_board
    GS->>GS: is_game_over() returns false
    
    opt AI Move
        GS->>+A: get_best_move(board)
        A-->>-GS: ai_move
        GS->>+S: simulate_move(board, ai_move)
        S-->>-GS: new_board
        GS->>GS: new_board.flip_board()
        GS->>GS: Update self.board with new_board
        GS->>GS: is_game_over() returns false
    end

    GS-->>-GW: Return updated board state
    GW->>GW: render()
    Note over GW: Waiting for the next move
```
