from entities.board import Board
from services.game_service import GameService

def main():
    board = Board("black")
    game_service = GameService(board)
    
    print(game_service.move_piece((6,2), (4,2)))
    print(game_service.move_piece((6,0), (5,0)))
    
    print(game_service.move_piece((4,2), (3,2)))
    print(game_service.move_piece((5,0), (3,0)))
    print(game_service.move_piece((5,0), (4,0)))
    
    print(game_service.move_piece((3,2), (2,2)))
    print(game_service.move_piece((4,0), (3,0)))
    
    print(game_service.score)
    
    print(game_service.move_piece((2,2), (1,2)))
    print(game_service.move_piece((2,2), (1,3)))
    
    print(game_service.score)
    
    
main()