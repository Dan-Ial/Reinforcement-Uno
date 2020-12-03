from game import Game

class Train:
    def __init__(self):
        epsilon = 1

    # reference of the qlearning algorithm
    #todo- will mkae it applicable to the uno environment
    def q_learning_algo(transition_states, reward, starting_point, destination, move_type, total_state_size, alpha, gamma, epsilon, total_number_of_episodes):
        """
        Applies the q_value learning algorithm
        :param transition_states: Transition states
        :param reward: rewards
        :param starting_point: Starting point
        :param destination: Goal
        :param move_type: Actions
        :param total_state_size: State
        :param alpha: learning rate (set at 0.5)
        :param gamma: set at 1
        :param epsilon: set at 0.1
        :param total_number_of_episodes: the amount of episode loops
        :param total_rows: row
        :param total_columns: column
        :return: the amount of steps required in one episode (to reach the goal)
        """
        total_columns = 10
        total_rows = 7
        Q = [[0 for _ in range(move_type)] for _ in range(total_state_size)]
        possibilities = 3 if move_type == 8 else 1
        J, K = 0, 1
        states_visited = [[0 for _ in range(total_columns)] for _ in range(total_rows)]
        steps_in_one_episode = []
        for _ in tqdm(range(total_number_of_episodes)):
            I = 0
            s = starting_point
            states_visited[s // 10][s % 10] += 1
            while s != destination:
                which_wind = randint(0, possibilities - 1)
                a = epsilon_greedy(Q[s], epsilon, K, move_type)
                s1 = transition_states[s][a][which_wind]
                r = reward[s1]
                Q[s][a] = Q[s][a] + alpha * (r + gamma * max(Q[s1]) - Q[s][a])
                s = s1
                J += 1
                I += 1
                states_visited[s // 10][s % 10] += 1
            K += 1
            steps_in_one_episode.append(I)
        move_kind = "Stochastic & King's" if move_type == 8 else "Non Stochastic & Peasant's"
        graph(states_visited, "Q Learning: " + move_kind + " Moves")
        optimal_policy(Q, starting_point, destination)
        return steps_in_one_episode