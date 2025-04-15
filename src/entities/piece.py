class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        match type:
            case "pawn":
                self.value = 1
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
        if self.type != "knight":
            return self.color[0] + self.type[0].capitalize()
        else:
            return self.color[0] + "N"
