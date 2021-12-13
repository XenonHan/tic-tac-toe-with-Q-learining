"""
Author: Han Chi Chiu
Last modify: 25/11/2021
"""
import random
import sys
import pickle

last_play = None  # ai, human or trainer

# first create the game board
board = [0] * 9
play_history = []
numRound = 0
winner = None
train_num = 0
epsilon = 0  # play with you, human, I need to use full power
try:
    with open('checkpoint', 'rb') as f:
        q_table = pickle.load(f)
except FileNotFoundError:
    print("It seems the checkpoint file broken or disappear, please download a new one")
    q_table = {}

# print(q_table)


# we need a function to print the board
def print_board(player):
    global numRound
    numRound += 1
    print("Round %d: " % numRound)
    print(player, "picks: \n")
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("")
            if i != 2 and i != 8:
                print('─' * 11)
        if i % 3 == 1:
            print('│', end="")
        if board[i] == 0:
            print('   ', end="")
        elif board[i] == 1:
            print(' X ', end="")
        elif board[i] == -1:
            print(' O ', end="")
        if i % 3 == 1:
            print('│', end="")
    print("\n")


# This is the Q learning class with epsilon greedy policy
class QLearn:
    def __init__(self, alpha=0.1, gamma=1):
        self.alpha = alpha
        self.gamma = gamma

    # this function return the largest and smallest q value (state, action), random if multiple options
    def get_qValue(self, state):
        # print("state: ", state)
        target = q_table.get(state)
        if target is not None:
            max_value = max(target)
            max_list = [i for i in range(len(target)) if target[i] == max_value and board[i] == 0]
            if max_list:
                max_index = random.choice(max_list)  # the max index is for following the q learning table
            else:
                max_index = random.choice([i for i in range(len(target)) if board[i] == 0])  # this is at least one

            random_list = [i for i in range(len(target)) if target[i] < max_value and board[i] == 0]
            if random_list:
                random_index = random.choice(random_list)  # a random index
            else:
                random_index = random.choice([i for i in range(len(target)) if board[i] == 0])  # this is at least one
        else:
            q_table[state] = [0] * 9
            target = q_table[state]

            max_index = random_index = random.choice(
                [i for i in range(len(target)) if board[i] == 0])  # this also at least one

        return max_index, random_index

    def next_action(self, state):
        greedy_action, random_action = self.get_qValue(state)
        random_num = random.random()
        if random_num < epsilon:
            # print("ai next random_action: ", random_action)
            return random_action
        else:
            # print("ai next greedy_action: ", greedy_action)
            return greedy_action

    def learn_q(self, history, reward):
        if last_play != 'ai':
            history = history[:len(history) - 1]

        # update the last step before terminal case
        last_step = history[len(history) - 1]
        target = tuple(history[: len(history) - 1])
        last_record = record = q_table.get(target)
        old_q = record[last_step]
        record[last_step] = (((1 - self.alpha) * old_q) + (self.alpha * self.gamma * reward))
        history = history[:len(history) - 1]  # human
        history = history[:len(history) - 1]  # ai
        # print("last_step: ",last_step,end=" ")

        # recursive update the previous steps
        while history:
            last_step = history[len(history) - 1]
            # print(last_step, end=" ")
            target = tuple(history[: len(history) - 1])
            record = q_table.get(target)
            old_q = record[last_step]
            max_next_q = max(last_record)  # the max q value for the next step
            # print("max_next_q: ", max_next_q)
            record[last_step] = (((1 - self.alpha) * old_q)
                                 + (self.alpha * self.gamma * (
                            max_next_q - old_q)))  # reward for this step is 0 as not win/loss
            # print("record[last_step]: ", record[last_step])
            last_record = record
            history = history[:len(history) - 1]  # human
            history = history[:len(history) - 1]  # ai


# check the game state
def check_win(symbol):
    count = 0
    # check horizontal line
    while count <= 9:
        sum_value = sum(board[count:count + 3])
        if sum_value == 3 or sum_value == -3:
            if sum_value * symbol > 0:
                return "win"
            else:
                return 'loss'
        count += 3

    count = 0
    # check vertical line
    while count <= 3:
        sum_value = sum([board[i] for i in range(9) if i % 3 == count])
        if sum_value == 3 or sum_value == -3:
            if sum_value * symbol > 0:
                return "win"
            else:
                return "loss"
        count += 1

    # check diagonal lines
    sum_value = board[0] + board[4] + board[8]
    if sum_value == 3 or sum_value == -3:
        if sum_value * symbol > 0:
            return "win"
        else:
            return "loss"
    sum_value = board[2] + board[4] + board[6]
    if sum_value == 3 or sum_value == -3:
        if sum_value * symbol > 0:
            return "win"
        else:
            return "loss"

    # check if draw
    if 0 not in board:
        return "draw"
    else:
        return "continue"


# We need a trainer to train the agent
class TrainPlayer:
    player_type = "You"

    def __init__(self, symbol):
        self.symbol = symbol
        self.symbol = symbol

    def draw(self):
        target = random.randint(0, 8)
        while board[target] != 0:
            target = random.randint(0, 8)
        board[target] = self.symbol
        play_history.append(target)
        global last_play
        last_play = "trainer"


# We need a human player
class HumanPlayer:
    player_type = "You"

    def __init__(self, symbol):
        self.symbol = symbol

    def draw(self):
        target = int(input("\n input the grid number you want to place (0 - 8): "))
        while board[target] != 0:
            target = int(input("\n input the grid number you want to place (0 - 8): "))
        board[target] = self.symbol
        play_history.append(target)
        global last_play
        last_play = "human"


# We also need an agent to learn how to play the game with Q-learning
class AiPlayer:
    player_type = "AI"

    def __init__(self, symbol):
        self.symbol = symbol
        self.ai = QLearn()

    def draw(self):
        # target = random.randint(0, 8)  # this will be replace by q learning
        state = tuple(play_history)
        reward = 0
        target = self.ai.next_action(state)
        board[target] = self.symbol
        play_history.append(target)
        global last_play
        last_play = "ai"

    def check_and_learn(self):
        game_process = check_win(self.symbol)

        # set the reward for each end game state
        global winner
        if game_process == "win":
            reward = 1
            winner = "AI won!"
            self.ai.learn_q(play_history, reward)
        elif game_process == "loss":
            reward = -1
            self.ai.learn_q(play_history, reward)
            winner = "You won!"
        elif game_process == "draw":
            reward = 0
            winner = "Draw!"
            self.ai.learn_q(play_history, reward)
        else:
            return


if __name__ == '__main__':
    order = int(input("input 1 if you want to play first, otherwise input 2: "))
    ai_player = None
    if order == 1:
        player_1 = HumanPlayer(1)
        ai_player = player_2 = AiPlayer(-1)
    elif order == 2:
        ai_player = player_1 = AiPlayer(1)
        player_2 = HumanPlayer(-1)
    elif order == 3:  # ai training mode
        random_role = random.randint(0, 1)
        if random_role == 1:
            ai_player = player_1 = AiPlayer(1)
            player_2 = TrainPlayer(-1)
        else:
            player_1 = TrainPlayer(1)
            ai_player = player_2 = AiPlayer(-1)

    if order == 1 or order == 2:
        while winner is None:
            player_1.draw()
            print_board(player_1.player_type)
            ai_player.check_and_learn()
            if winner:
                break
            player_2.draw()
            print_board(player_2.player_type)
            ai_player.check_and_learn()
    elif order == 3:
        epsilon = 0.7
        while epsilon > 0:
            while winner is None:
                player_1.draw()
                ai_player.check_and_learn()
                if winner:
                    break
                player_2.draw()
                ai_player.check_and_learn()

            play_history = []
            winner = None
            board = [0] * 9
            numRound = 0

            epsilon -= 0.000000007  # this number is for fun only
            train_num += 1
    # print("train_num: ", train_num)

    print(winner)
    # print(q_table)
    # print(play_history)

    with open('checkpoint', 'wb') as f:
        pickle.dump(q_table, f)
