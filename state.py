class State:
    def __init__(self, playable):
        self.playable = playable.copy()
        self.action_values = []
        for card in self.playable:
            self.action_values.append(1)

        self.action_values.append([1, 1, 1, 1]) # value of choosing r, g, b, y if a black card is played

    def __str__(self):
        outstr = "Playable cards: "
        for card in self.playable:
            outstr += card.type + " " + card.colour + " "

        return outstr

    def __eq__(self, other):
        if len(self.playable) != len(other.playable):
            return False

        for card1 in other.playable:
            card_present = False
            for card2 in self.playable:
                if card1 == card2:
                    card_present = True

            if not card_present:
                return False

        for card1 in self.playable:
            card_present = False
            for card2 in other.playable:
                if card1 == card2:
                    card_present = True

            if not card_present:
                return False

        return True
