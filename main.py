"""
Class: CISC 453/474
Professor: Sydney Givigi
Authors: Shreyansh Anand, Anne Liu, Bennet Montgomery, Daniel Oh
"""

from game import Game
# from test import Test
from state import State
from card import Card

results_from_training = []
results_from_testing = []


def game_loop(g):


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
    # print("round: " + str(turn//4))
    # print("winner: " + str(g.current_player))
        # results_from_training.append((g.current_player, turn//4))
        # results_from_testing.append((g.current_player, turn//4))
    return g.current_player, turn // 4


def testing():
    g = Game(True)
    count_times_1_wins_total = 0
    for _ in range(100):
        count_times_1_wins = 0
        print("Epoch: " + str(_))
        print("educating")
        for i in range(50):
            g.training = True
            g.restart_game()
            g.init_cards()
            g.distribute_cards()
            game_loop(g)
        print("---------------")
        print("3 other uneducated agents")
        for i in range(50):
            g.training = False
            g.restart_game()
            g.init_cards()
            g.distribute_cards()
            current_player, turn = game_loop(g)
            if current_player == 1:
                count_times_1_wins += 1
                count_times_1_wins_total += 1
        print(count_times_1_wins/50)
        print(count_times_1_wins_total/(50 * (_+1)))
        print("\n")


def main():
    # for _ in range(1000):
    #     print("Game: " + str(_))
    #     game_loop(True)
    #     print("\n")

    test_q = [State([Card("red", "reverse"), Card("blue", "9")])]
    test = State([Card("blue", "9"), Card("red", "reverse")])
    print(test in test_q)
    testing()

    # print(results)
    # for stats
    # data = Counter(results)
    # print(data.most_common())  # Returns all unique items and their counts
    # print("winner most often is: " + str(data.most_common(1)))  # Returns the highest occurring item


if __name__ == '__main__':
     main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
