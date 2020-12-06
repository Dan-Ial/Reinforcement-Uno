from card import Card
from state import State
from random import shuffle, randint, random
import copy


class Game:
    def __init__(self):
        self.players = {1: [], 2: [], 3: [], 4: []}
        self.previous_hand = {1: None, 2: None, 3: None, 4: None}
        self.turn = 0
        self.turn_order = "CW"
        self.draw_from = []
        self.played = []
        self.current_player = randint(1, 5)
        self.colour_to_play = ""

        #RL parameters
        self.qtable = []
        self.epsilon = 0.25
        self.alpha = 0.1

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

        for player in self.players:
            self.qtable.append(State(self.get_playable_cards(player)))

        self.current_player = 1

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

    def able_to_play(self, player, myturn=True):
        """
        function to check if the player can play on the last card
        :param player:
        :return:
        """
        card_to_play_on = self.played[-1]
        for card in (self.players[player]):
            if card.colour == self.colour_to_play or card.type == card_to_play_on.type or card.colour == "black":
                if myturn:
                    return True
                elif card.type == "draw 2" or card.type == "draw 4":
                    return True

        return False

    def get_playable_cards(self, player=None):
        if player is None:
            player = self.current_player

        playable_cards = []

        card_to_play_on = self.played[-1]
        for card in (self.players[player]):
            if card.colour == card_to_play_on.colour or card.type == card_to_play_on.type or card.colour == "black":
                if card_to_play_on.type == "draw 4" or card_to_play_on.type == "draw 2":
                    if card.type == "draw 4" or card.type == "draw 2":
                        playable_cards.append(card)
                else:
                    playable_cards.append(card)

        return playable_cards

    # method for assessing the hand of the current player and choosing a card to play
    def assess_hand(self, player=None):
        if player is None:
            player = self.current_player

        # searching for hand in qtable
        player_hand = State(self.get_playable_cards(player))
        player_hand_visited = False
        for hand in self.qtable:
            if player_hand == hand:
                player_hand_visited = True
                player_hand = hand

        # adding hand to qtable if not visited
        if not player_hand_visited:
            self.qtable.append(player_hand)

        # setting hand to previous hand for this player
        self.previous_hand[player] = player_hand

        # select card with e-greedy
        if random() < self.epsilon:
            if len(player_hand.action_values) > 1:
                action = randint(0, len(player_hand.action_values) - 2)
            else:
                action = -1 # draw a card
        else:
            action = player_hand.action_values[:-2].index(max(player_hand.action_values[:-2]))

        # play selected card:
        if action == -1: # draw a card
            self.draw(player, 1)
            return "drew a card"
        if player_hand.playable[action].colour == "black":
            # decide what colour to switch to using e-greedy
            if random() < self.epsilon:
                colour = randint(0, 3)
            else:
                colour = player_hand.action_values[-1].index(max(player_hand.action_values[-1]))

            if colour == 0:
                self.play_card(player, player_hand.playable[action], "red")
            elif colour == 1:
                self.play_card(player, player_hand.playable[action], "green")
            elif colour == 3:
                self.play_card(player, player_hand.playable[action], "blue")
            else:
                self.play_card(player, player_hand.playable[action], "yellow")

            return "picked " + player_hand.playable[action].type + " and changed the colour to " + self.colour_to_play
        else: # a non-black card was played
            self.play_card(player, player_hand.playable[action])
            return "picked " + player_hand.playable[action].type + " " + player_hand.playable[action].colour

    def play_card(self, player, card_selected, colour_selected=None):
        """
        function for when a player plays an actual card
        :param player:
        :param card_selected:
        :param colour_selected:
        :return:
        """
        self.played.append(copy.copy(card_selected))
        del self.players[player][self.players[player].index(card_selected)]
        if self.played[-1].type == "skip:":
            self.current_player += 1

        # if player chooses to play a draw 4 or draw 2 card, it gets a little complicated
        if self.played[-1].type == "draw 4" or self.played[-1].type == "draw 2":
            draw_total = 4 if self.played[-1].type == "draw 4" else 2

            # determine total number of cards to be drawn
            for i in range(len(self.played) - 2, -1, -1):
                if self.played[i] == "draw 4":
                    draw_total += 4
                elif self.played[i] == "draw 2":
                    draw_total += 2
                else:
                    break

            if colour_selected is not None:
                self.colour_to_play = colour_selected

            self.current_player += 1 # check next player
            if not self.able_to_play(self.current_player):  # i.e. next player doesn't have a draw 2 or draw 4 to pass
                self.draw(self.current_player, draw_total)
            else:
                self.current_player -= 1 # reset player count (it's not their turn yet!)

        if self.played[-1].type == "wild":
            """colour to be selected by the player"""
            self.colour_to_play = colour_selected

        if self.played[-1].type == "reverse":
            self.turn_order = "CW" if self.turn_order == "CCW" else "CCW"

        # colour change sanity check
        if self.played[-1].colour != "black":
            self.colour_to_play = self.played[-1].colour

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
