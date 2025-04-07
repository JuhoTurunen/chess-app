class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        match type:
            case "pawn":
                self.value = 1
                self.has_jumped = False
            case "knight":
                self.value = 3
            case "bishop":
                self.value = 3
            case "rook":
                self.value = 5
                self.has_moved = False
            case "queen":
                self.value = 9
            case "king":
                self.value = 20
                self.has_moved = False
    
    def __repr__(self):
        return self.color[0] + self.type[0].capitalize()