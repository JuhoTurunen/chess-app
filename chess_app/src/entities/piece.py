class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
    
    def __repr__(self):
        return self.color[0] + self.type[0].capitalize()