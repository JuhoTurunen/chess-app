class Piece:
    """Represents a chess piece.

    Attributes:
        color: String for piece color.
        rank: String for the type of the piece (e.g. "knight").
        value: The integer value of the piece.
        has_moved: Boolean for whether the piece has moved (only for king and rook).
    """

    def __init__(self, color, rank):
        """Initializes piece with color and type.

        Args:
            color: String for piece color.
            rank: String for the type of the piece (e.g. "knight").
        """
        self.color = color
        self.rank = rank
        match rank:
            case "pawn":
                self.value = 100
            case "knight":
                self.value = 320
            case "bishop":
                self.value = 330
            case "rook":
                self.value = 510
                self.has_moved = False
            case "queen":
                self.value = 975
            case "king":
                self.value = 0
                self.has_moved = False

    def __repr__(self):
        if self.rank != "knight":
            return self.color[0] + self.rank[0].capitalize()
        return self.color[0] + "N"
