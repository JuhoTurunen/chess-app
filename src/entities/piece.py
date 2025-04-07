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
            case "queen":
                self.value = 9
            case "king":
                self.value = 10
    
    def __repr__(self):
        return self.color[0] + self.type[0].capitalize()