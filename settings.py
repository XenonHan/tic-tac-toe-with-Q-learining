""""
This file contain the global parameters share among different classes
"""
board = [0] * 9
play_history = []
epsilon = 0
last_play = None
game_winner = None
ai_turn = False
grids = []


def reset():
    global board, play_history, epsilon, last_play, game_winner, ai_turn
    board = [0] * 9
    play_history = []
    epsilon = 0
    last_play = None
    ai_turn = False
    game_winner = None
