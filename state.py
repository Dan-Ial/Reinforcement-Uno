class State:
    def __init__(self, playable):
        self.playable = playable
        self.action_values = []
        for card in self.playable:
            self.action_values.append(1)

    def update_action_values(self, new_val):
        self.action_values = new_val

    def get_action_values(self):
        return self.action_values

    def __eq__(self, other):
        for card in other.playable:
            if card not in self.playable:
                return False

        for card in self.playable:
            if card not in other.playable:
                return False

        return True