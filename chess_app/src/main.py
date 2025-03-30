from entities.board import Board
from services.game_service import GameService

def main():
    board = Board("black")
    game_service = GameService(board)
    
    print(game_service.move_piece((6,2), (5,2)))
    print(game_service.move_piece((6,2), (5,2)))
    print(game_service.move_piece((5,2), (4,2)))
    print(game_service.move_piece((5,2), (4,2)))
    print(game_service.move_piece((4,2), (3,2)))
    print(game_service.move_piece((4,2), (3,2)))
    
main()