from card import Card
from state import State
from random import shuffle, randint, random
import copy


class Game:
    def __init__(self, training):
        self.players = {1: [], 2: [], 3: [], 4: []}
        self.previous_play = {1: (State([]), [-2], []), 2: (State([]), [-2], []), 3: (State([]), [-2], []),
                              4: (State([]), [-2], [])}
        self.turn = 0
        self.turn_order = "CW"
        self.draw_from = []
        self.played = []
        self.current_player = randint(1, 5)
        self.colour_to_play = ""
        self.must_play_draw = False

        # RL parameters
        self.qtable = []
        self.epsilon = 0.25
        self.alpha = 0.1
        self.gamma = 1.0

        # Training
        self.training = training
        self.draw_reward = -5
        self.play_reward = 0
        self.win_reward = 10

    def restart_game(self):
        """
        method to restart the game at the end of each training/testing round
        :return:  a game that is restarted everywhere except in the qtable/reward.
        """
        self.players = {1: [], 2: [], 3: [], 4: []}
        self.previous_play = {1: (State([]), [-1], []), 2: (State([]), [-1], []), 3: (State([]), [-1], []),
                              4: (State([]), [-1], [])}
        self.turn = 0
        self.turn_order = "CW"
        self.draw_from = []
        self.played = []
        self.current_player = randint(1, 5)
        self.colour_to_play = ""
        self.must_play_draw = False

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
        #  ensure that the first card played is not a draw 4.
        while self.draw_from[0].type == "draw 4":
            shuffle(self.draw_from)
        self.played.append(self.draw_from[0])
        del self.draw_from[0]
        self.colour_to_play = self.played[-1].colour

        for player in self.players:
            self.qtable.append(State(self.get_playable_cards(player)))

        self.current_player = 1

    def draw(self, player, number_to_draw=0):
        """
        function for when a player needs to draw
        :param number_to_draw: if the default value is 0 then that means they need to draw till a playable card is found
        :param player:
        :return:
        """
        if number_to_draw == 0:
            while not self.able_to_play(player):
                if len(self.draw_from) == 0:
                    # if there are no cards left to be drawn from, remake the pile
                    last_played = self.played[-1]
                    del self.played[-1]
                    shuffle(self.played)
                    self.draw_from = self.played.copy()
                    self.played = [last_played]
                self.players[player].append(self.draw_from[0])
                del self.draw_from[0]
        else:
            for _ in range(number_to_draw):
                if len(self.draw_from) == 0:
                    # if there are no cards left to be drawn from, remake the pile
                    last_played = self.played[-1]
                    del self.played[-1]
                    shuffle(self.played)
                    self.draw_from = self.played.copy()
                    self.played = [last_played]
                self.players[player].append(self.draw_from[0])
                del self.draw_from[0]
        return True

    def able_to_play(self, player, myturn=True):
        """
        function to check if the player can play on the last card
        :param player: current player
        :param myturn: if the current player is playing or if its for the next player
        :return: true or false
        """
        card_to_play_on = self.played[-1]
        for card in (self.players[player]):
            if card.colour == self.colour_to_play or card.type == card_to_play_on.type or card.colour == "black":
                if myturn:
                    return True
                elif card.type == "draw 2" and card_to_play_on.type == "draw 2":
                    return True
                elif card.type == "draw 4" and card_to_play_on.type == "draw 4":
                    return True

        return False

    def get_playable_cards(self, player=None):
        """
        function to see what cards a player can play
        :param player: player to check
        :return: a list of cards a player can play
        """
        if player is None:
            player = self.current_player

        playable_cards = []

        card_to_play_on = self.played[-1]
        for card in (self.players[player]):
            if card.colour == self.colour_to_play or card.type == card_to_play_on.type or card.colour == "black":
                if self.must_play_draw and card_to_play_on.type == "draw 4" and card.type == "draw 4":
                    playable_cards.append(card)
                elif self.must_play_draw and card_to_play_on.type == "draw 2" and card.type == "draw 2":
                    playable_cards.append(card)
                else:
                    playable_cards.append(card)

        self.must_play_draw = False
        return playable_cards

    def update_q_table(self, s, state_prime, reward, action, colour_index=None, terminal=False):
        #  method to update the q_table using the algorithms provided in class
        if state_prime in self.qtable and not terminal:
            state_prime = self.qtable[self.qtable.index(state_prime)]

        if len(state_prime.action_values) > 1:
            self.qtable[s].action_values[action] += self.alpha * (
                    reward + self.gamma * max(state_prime.action_values[:-1]) - self.qtable[s].action_values[action])

        if colour_index is not None:
            if len(state_prime.action_values) > 1:
                self.qtable[s].action_values[-1][colour_index] += self.alpha * (
                        reward + self.gamma * max(state_prime.action_values[:-1]) -
                        self.qtable[s].action_values[-1][colour_index])

        if terminal:
            self.qtable[s].action_values[action] += self.alpha * (reward - self.qtable[s].action_values[action])

    # method for assessing the hand of the current player and choosing a card to play
    def assess_hand(self, player=None):
        if player is None:
            player = self.current_player

        if self.colour_to_play == "black" and self.previous_play[1] == [-1]:
            if random() < self.epsilon:
                colour = randint(0, 3)
            else:
                poss_colours = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
                hand = self.players[player]
                for card in hand:
                    if card.colour in poss_colours.keys():
                        poss_colours[card.colour] += 1
                colour = max(poss_colours, key=poss_colours.get)
            self.colour_to_play = colour

        # searching for hand in qtable
        player_hand = State(self.get_playable_cards(player))
        player_hand_visited = False
        for hand in self.qtable:
            if player_hand == hand:
                player_hand_visited = True
                break

        # adding hand to qtable if not visited
        if self.training:
            if not player_hand_visited:
                self.qtable.append(player_hand)

        # updating state/action value of previous hand using
        # Q(S, A) -> Q(S, A) + alpha[R + gamma*maxa(Q(S', a)) - Q(S, A)], where
        #   S ::= previous hand
        #   S' ::= this hand
        #   a ::= most valued action in this hand
        #   A ::= action played
        #   alpha ::= step size
        #   R ::= number of cards in the previous hand - number of cards in this hand
        #   gamma ::= 1 (finite game)
        first_turn = False
        s = None
        a = None
        c_a = None

        if self.previous_play[player][1][0] >= 0 and self.training:
            s = self.qtable.index(self.previous_play[player][0])
            a = self.previous_play[player][1][0]
            if len(self.previous_play[player][1]) > 1:
                c_a = self.previous_play[player][1][1]
        elif self.previous_play[player][1] == [-2] and self.training:  # first hand of the game
            first_turn = True
            """
            R = len(self.previous_play[player][2]) - len(self.players[player])

            # updating card selection value
            if len(player_hand.action_values[:-1]) > 0:
                self.qtable[s].action_values[a] = self.qtable[s].action_values[a] + self.alpha * (
                            R + self.gamma * max(player_hand.action_values[:-1]) - self.qtable[s].action_values[a])

            # updating colour choice value if a colour choice was made
            if len(self.previous_play[player][1]) > 1:
                a_c = self.previous_play[player][1][1]
                self.qtable[s].action_values[-1][a_c] = self.qtable[s].action_values[-1][a_c] + self.alpha * \
                                                        (R + self.gamma * max(player_hand.action_values[-1])
                                                         - self.qtable[s].action_values[-1][a_c])
            """

        # select card with e-greedy

        if self.training:
            if len(player_hand.action_values) > 1:
                if random() < self.epsilon:
                    action = randint(0, len(player_hand.action_values) - 2)
                else:
                    action = player_hand.action_values[:-1].index(max(player_hand.action_values[:-1]))
            else:
                action = -1  # draw a card

        # testing purposes
        elif not self.training:
            # first player plays optimally
            if player == 1:
                if len(player_hand.action_values) > 1:
                    if random() < self.epsilon:
                        action = randint(0, len(player_hand.action_values) - 2)
                    else:
                        action = player_hand.action_values[:-1].index(max(player_hand.action_values[:-1]))
                else:
                    action = -1  # draw a card

            # others players will always use random action
            else:
                if len(player_hand.action_values) > 1:
                    action = randint(0, len(player_hand.action_values) - 2)
                else:
                    action = -1  # draw a card

        # play selected card:
        if action == -1:  # draw a card
            self.draw(player)  # todo investigate if we make this unlimited till you can play

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

            # applying q table update
            if self.training and s is not None and not first_turn:
                if c_a is not None:
                    self.update_q_table(s, player_hand, self.draw_reward, a, c_a)
                else:
                    self.update_q_table(s, player_hand, self.draw_reward, a)

            self.previous_play[player] = (player_hand, [-1], self.players[player].copy())

            return "drew a card"
        if player_hand.playable[action].colour == "black":
            # decide what colour to switch to using e-greedy
            if random() < self.epsilon:
                colour = randint(0, 3)
            else:
                colour = player_hand.action_values[-1].index(max(player_hand.action_values[-1]))

            # applying q table update
            if self.training and s is not None and not first_turn:
                if c_a is not None:
                    self.update_q_table(s, player_hand, self.play_reward, a, c_a)
                else:
                    self.update_q_table(s, player_hand, self.play_reward, a)

            # setting hand to previous hand for this player
            self.previous_play[player] = (player_hand, [action, colour], self.players[player].copy())

            if colour == 0:
                self.play_card(player, player_hand.playable[action], "red")
            elif colour == 1:
                self.play_card(player, player_hand.playable[action], "green")
            elif colour == 3:
                self.play_card(player, player_hand.playable[action], "blue")
            else:
                self.play_card(player, player_hand.playable[action], "yellow")

            return "played " + player_hand.playable[action].type + " and changed the colour to " + self.colour_to_play
        else:  # a non-black card was played
            # applying q-table update
            # applying q table update
            if self.training and s is not None and not first_turn:
                if c_a is not None:
                    self.update_q_table(s, player_hand, self.play_reward, a, c_a)
                else:
                    self.update_q_table(s, player_hand, self.play_reward, a)

            self.previous_play[player] = (player_hand, [action], self.players[player].copy())
            self.play_card(player, player_hand.playable[action])
            return "played " + player_hand.playable[action].type + " " + player_hand.playable[action].colour

    def play_card(self, player, card_selected, colour_selected=None):
        """
        function for when a player plays an actual card
        :param player: current player that is playing
        :param card_selected: the card they will be playing
        :param colour_selected: the colour that will be played if it is to change because of a Wild
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
                if self.played[i].type == "draw 4":
                    draw_total += 4
                elif self.played[i].type == "draw 2":
                    draw_total += 2
                else:
                    break

            if colour_selected is not None:
                self.colour_to_play = colour_selected

            if self.turn_order == "CW":  # check next player
                if self.current_player == 4:
                    self.current_player = 1
                else:
                    self.current_player += 1
            else:
                if self.current_player == 1:
                    self.current_player = 4
                else:
                    self.current_player -= 1

            if not self.able_to_play(self.current_player,
                                     False):  # i.e. next player doesn't have a draw 2 or draw 4 to pass
                self.draw(self.current_player, draw_total)
            else:
                self.must_play_draw = True

                if self.turn_order == "CW":
                    if self.current_player == 1:
                        self.current_player = 4
                    else:
                        self.current_player -= 1
                else:
                    if self.current_player == 4:
                        self.current_player = 1
                    else:
                        self.current_player += 1

        if self.played[-1].type == "wild":
            """colour to be selected by the player"""
            self.colour_to_play = colour_selected

        if self.played[-1].type == "reverse":
            self.turn_order = "CW" if self.turn_order == "CCW" else "CCW"

        # colour change sanity check
        if self.played[-1].colour != "black":
            self.colour_to_play = self.played[-1].colour

        if len(self.players[player]) == 0 and self.training:
            if len(self.previous_play[player][1]) > 1:
                self.update_q_table(self.qtable.index(self.previous_play[player][0]), State([]), self.win_reward,
                                    self.previous_play[player][1][0], self.previous_play[player][1][1], True)
            else:
                self.update_q_table(self.qtable.index(self.previous_play[player][0]), State([]), self.win_reward,
                                    self.previous_play[player][1][0], terminal=True)

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
