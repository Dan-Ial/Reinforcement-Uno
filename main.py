"""
Class: CISC 453/474
Professor: Sydney Givigi
Authors: Shreyansh Anand, Anne Liu, Bennet Montgomery, Daniel Oh
"""

from game import Game
from state import State
from card import Card


def main():
    g = Game()
    g.init_cards()
    g.distribute_cards()

    # sanity check
    print("Initial card: ")
    print(g.played[0].type)
    print(g.played[0].colour)
    print("Player hands: ")
    for i in range(1, 5):
        print(str(State(g.players[i])))

    print("Player playable cards: ")
    for i in range(1, 5):
        print(str(State(g.get_playable_cards(i))))

    print(g.assess_hand())



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
