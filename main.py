"""
Class: CISC 453/474
Professor: Sydney Givigi
Authors: Shreyansh Anand, Anne Liu, Bennet Montgomery, Daniel Oh
"""

from game import Game
from test import Test
from state import State
from card import Card
from collections import Counter

results = []

def game_loop(training):
    g = Game(training)
    g.init_cards()
    g.distribute_cards()

    # sanity check
    # print("Initial card: ")
    # print(g.played[0].type)
    # print(g.played[0].colour)
    # print("Player hands: ")
    # for i in range(1, 5):
    #     print(str(State(g.players[i])))

    # print("Player playable cards: ")
    # for i in range(1, 5):
    #     print(str(State(g.get_playable_cards(i))))

    # Shrey's code -> termination statement, keep going till at least one player has 0 cards
    turn = 0
    while len(g.players[g.current_player]) != 0:
        # print(g.current_player)
        # print(str(State(g.get_playable_cards(g.current_player))))
        # print(g.assess_hand())
        g.assess_hand()
        turn += 1
    print("round: " + str(turn//4))
    print("winner: " + str(g.current_player))
    results.append(g.current_player)


def testing():
    for _ in range(100):
        for _ in range(1000):
            game_loop(True)
        print("educating")
        print("---------------")
        for _ in range(100):
            game_loop(False)
        print("uneducated agents")
        print("\n")


def main():
    # for _ in range(1000):
    #     print("Game: " + str(_))
    #     game_loop(True)
    #     print("\n")

    testing()

    # print(results)
    #for stats
    data = Counter(results)
    print(data.most_common())  # Returns all unique items and their counts
    print("winner most often is: "+ str(data.most_common(1)))  # Returns the highest occurring item



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
