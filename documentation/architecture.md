# Architecture

This is a general, high-level class diagram for the chess engine:
```mermaid
classDiagram
    %% Main UI components
    class MainMenu {
      +run()
      +handle_events()
      +render()
    }
    class GameWindow {
      +run()
      +handle_events()
      +render()
    }

    %% Core game logic/service
    class GameService {
      +move_handler(move)
      +move_piece(move)
    }

    %% Game entities
    class Board {
      +get_piece(position)
      +set_piece(position, piece)
      +flip_board()
    }
    class Piece {
      <<entity>>
      +color
      +type
    }

    %% AI engine
    class AiEngine {
      +get_best_move(board)
      +negamax(board, depth, alpha, beta)
    }

    %% Relationships
    MainMenu --> GameService : provides config for
    GameWindow --> GameService : uses
    GameService --> Board : operates on
    Board --> Piece : contains
    GameService o--> AiEngine : optional dependency

```

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
