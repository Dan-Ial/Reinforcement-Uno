from card import Card
from random import shuffle, randint


class Game:
    def __init__(self):
        self.players = {1: [], 2: [], 3: [], 4: []}
        self.turn = 0
        self.turn_order = "CW"
        self.draw_from = []
        self.played = []
        self.current_player = randint(1, 5)
        self.colour_to_play = ""

    def init_cards(self):
        """
        The deck consists of 108 cards: four each of "Wild" and "Wild Draw Four," and 25 each of four different colors
        (red, yellow, green, blue). Each color consists of one zero, two each of 1 through 9, and two each
         of "Skip," "Draw Two," and "Reverse." These last three types are known as "action cards."
        :return:
        """
        types_of_card = [str(x) for x in range(10)]
        types_of_card += ["reverse", "skip", "draw 2"]
        colour = ["red", "green", "blue", "yellow"]
        for specific_colour in colour:
            for card_type in types_of_card:
                if card_type == "0":
                    self.draw_from.append(Card(specific_colour, card_type))
                else:
                    self.draw_from.append(Card(specific_colour, card_type))
                    self.draw_from.append(Card(specific_colour, card_type))
        special_cards = ["draw 4", "wild"]
        for card_type in special_cards:
            for _ in range(4):
                self.draw_from.append(Card("black", card_type))

    def distribute_cards(self):
        shuffle(self.draw_from)
        for player in self.players:
            for _ in range(7):
                self.players[player].append(self.draw_from[0])
                del self.draw_from[0]
        self.played.append(self.draw_from[0])
        del self.draw_from[0]
        self.colour_to_play = self.played[-1].colour

    def draw(self, player, number_to_draw=0):
        """
        function for when a player needs to draw
        :param number_to_draw: if the default value is 0, then that means they need to draw infinitely
        :param player:
        :return:
        """
        if number_to_draw == 0:
            while not self.able_to_play(player):
                if len(self.draw_from) == 0:
                    shuffle(self.played)
                    self.draw_from = self.played.copy()
                    self.played = []
                self.players[player] += self.draw_from[0]
                del self.draw_from[0]
        else:
            for _ in range(number_to_draw):
                if len(self.draw_from) == 0:
                    shuffle(self.played)
                    self.draw_from = self.played.copy()
                    self.played = []
                self.players[player] += self.draw_from[0]
                del self.draw_from[0]
        return True

    def able_to_play(self, player):
        """
        function to check if the player can play on the last card
        :param player:
        :return:
        """
        card_to_play_on = self.played[-1]
        for card in (self.players[player]):
            if card.colour == card_to_play_on.colour or card.type == card_to_play_on.type or card.colour == "black":
                return True
        return False

    def play_card(self, player, card_selected_index, colour_selected=None):
        """
        function for when a player plays an actual card
        :param player:
        :param card_selected_index:
        :param colour_selected:
        :return:
        """
        self.played.append(self.players[player][card_selected_index])
        del self.players[player][card_selected_index]
        if self.played[-1].type == "skip:":
            self.current_player += 1

        # todo stacking needs to be figured out, huge reward -> this will probably not happen here
        # if self.played[-1].type == "draw 4":
        #     self.current_player += 1
        #     self.draw(self.current_player, 4)
        #     self.colour_to_play = colour_selected

        if self.played[-1].type == "wild":
            """colour to be selected by the player"""
            self.colour_to_play = colour_selected

        # todo need to figure this one out -> need to give huge reward to put draw 2 after another ne
        # todo probably not gonna happen here
        # if self.played[-1].type == "draw 2":
        #     self.draw(self.current_player+, 4)
        #     self.colour_to_play = colour_selected

        if self.played[-1].type == "reverse":
            self.turn_order = "CW" if self.turn_order is "CCW" else "CCW"

        if self.turn_order == "CW":
            if self.current_player == 4:
                self.current_player = 1
            else:
                self.current_player += 1
        else:
            if self.current_player == 1:
                self.current_player = 4
            else:
                self.current_player -= 1
