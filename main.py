"""
Class: CISC 453/474
Professor: Sydney Givigi
Authors: Shreyansh Anand, Anne Liu, Bennet Montgomery, Daniel Oh
"""

from game import Game


def game_loop(g):
    """
    function to run the game once
    :param g: game to test on
    :return: the player that won the game, and how many rounds it took
    """
    # termination statement, keep going till at least one player has 0 cards
    turn = 0
    while len(g.players[g.current_player]) != 0:
        g.assess_hand()
        turn += 1
    return g.current_player, turn // 4


def testing():
    g = Game(True)  # initialize the game with training set to on as default
    print("No training:")
    count_times_1_wins_total = 0
    count_times_1_wins = 0
    for i in range(50):  # untrained see how the agent does when not trained at all in 50 games
        g.training = False
        g.restart_game()
        g.init_cards()
        g.distribute_cards()
        current_player, turn = game_loop(g)
        if current_player == 1:
            count_times_1_wins += 1
            count_times_1_wins_total += 1
    print(count_times_1_wins / 50)
    print(count_times_1_wins_total / 50)
    print("\n")
    for _ in range(1, 11):  # 10 epochs
        count_times_1_wins = 0
        print("Epoch: " + str(_))
        print("educating")
        for i in range(50):  # train in batches of 50
            g.training = True
            g.restart_game()
            g.init_cards()
            g.distribute_cards()
            game_loop(g)
        print("---------------")
        print("3 other uneducated agents")
        for i in range(50):  # test on 50 games and see how it improves against random agents over time
            g.training = False
            g.restart_game()
            g.init_cards()
            g.distribute_cards()
            current_player, turn = game_loop(g)
            if current_player == 1:
                count_times_1_wins += 1
                count_times_1_wins_total += 1
        print("This run: " + str(count_times_1_wins/50))
        print("Average run: " + str(count_times_1_wins_total/(50 * (_ + 1))))
        print("\n")


def main():
    testing()


if __name__ == '__main__':
    main()
