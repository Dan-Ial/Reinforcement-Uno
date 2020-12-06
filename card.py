class Card:
    def __init__(self, colour, type_of_card):
        self.colour = colour
        self.type = type_of_card

    def __eq__(self, other):
        return (self.colour == other.colour) and (self.type == other.type)