"""
Class: CISC 453/474
Professor: Sydney Givigi
Authors: Shreyansh Anand, Anne Liu, Bennet Montgomery, Daniel Oh
"""

from game import Game
from state import State
from card import Card


def game_loop():
    g = Game()
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


def main():
    print(State([Card("green", "5"), Card("green", "5")]) == State([Card("green", "5")]))

    for _ in range(1000):
        print("Game: " + str(_))
        game_loop()
        print("\n")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
