class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        match rank:
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
        if self.rank != "knight":
            return self.color[0] + self.rank[0].capitalize()
        return self.color[0] + "N"
