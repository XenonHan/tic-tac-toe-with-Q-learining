""""
This class is the AI agent that learn how to play the game by using Q-learning
The AI decide next action based on current game board state and the possible max reward action from Q-table
"""
import settings
from QLearning import QLearn
import game_board


class AI:
    def __init__(self):
        self.ai = QLearn()

    def draw(self):
        # target = random.randint(0, 8)  # this will be replace by q learning
        state = tuple(settings.play_history)
        target = self.ai.next_action(state)
        game_board.button_clicked(target)

    def check_and_learn(self):
        game_process = settings.game_winner

        # set the reward for each end game state
        if game_process == "AI":
            reward = 1
            self.ai.learn_q(settings.play_history, reward)
        elif game_process == "YOU":
            reward = -1
            self.ai.learn_q(settings.play_history, reward)
        elif game_process == "DRAW":
            reward = 0
        else:
            return

        self.ai.save()
