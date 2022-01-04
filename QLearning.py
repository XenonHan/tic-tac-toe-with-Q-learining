"""
The Q-learning in this implementation is done by Q-table in format:
{action_history, [prob. to take grid 0 - 8]}

Reward:
    win: +1
    loss: -1
    draw: 0
"""
import random
import pickle
import settings

class QLearn:
    q_table = None
    alpha = 0.03
    gamma = 1

    def __init__(self, alpha=None, gamma=None):
        self.alpha = alpha or self.alpha
        self.gamma = gamma or self.gamma
        try:
            with open('checkpoint', 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("No checkpoint detected, starting a baby AI ...")
            self.q_table = {}

    # this function return the largest and smallest q value (state, action), random if multiple options
    def get_qValue(self, state):
        # print("state: ", state)
        target = self.q_table.get(state)
        if target is not None:
            max_value = max(target)
            max_list = [i for i in range(len(target)) if target[i] == max_value and settings.board[i] == 0]
            if max_list:
                max_index = random.choice(max_list)  # the max index is for following the q learning table
            else:
                max_index = random.choice([i for i in range(len(target)) if settings.board[i] == 0])  # this is at least one

            random_list = [i for i in range(len(target)) if target[i] < max_value and settings.board[i] == 0]
            if random_list:
                random_index = random.choice(random_list)  # a random index
            else:
                random_index = random.choice([i for i in range(len(target)) if settings.board[i] == 0])  # this is at least one
        else:
            self.q_table[state] = [0] * 9
            target = self.q_table[state]

            max_index = random_index = random.choice(
                [i for i in range(len(target)) if settings.board[i] == 0])  # this also at least one

        return max_index, random_index

    def next_action(self, state):
        greedy_action, random_action = self.get_qValue(state)
        random_num = random.random()
        if random_num < settings.epsilon:
            # print("ai next random_action: ", random_action)
            return random_action
        else:
            # print("ai next greedy_action: ", greedy_action)
            return greedy_action

    def learn_q(self, history, reward):
        if settings.last_play != 'AI':
            history = history[:len(history) - 1]

        # update the last step before terminal case
        last_step = history[len(history) - 1]
        target = tuple(history[: len(history) - 1])
        last_record = record = self.q_table.get(target)
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
            record = self.q_table.get(target)
            old_q = record[last_step]
            max_next_q = max(last_record)  # the max q value for the next step
            # print("max_next_q: ", max_next_q)
            record[last_step] = (((1 - self.alpha) * old_q)
                                 + (self.alpha * self.gamma * (
                            max_next_q - old_q)))  # reward for this step is 0 as not win/loss
            last_record = record
            history = history[:len(history) - 1]  # human
            history = history[:len(history) - 1]  # ai

    # save record
    def save(self):
        with open('checkpoint', 'wb') as f:
            pickle.dump(self.q_table, f)
