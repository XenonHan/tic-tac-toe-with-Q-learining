"""
This is the tic tac toc game board
"""
import future.moves.tkinter as tk
import future.moves.tkinter.messagebox as mg
from PIL import Image, ImageTk
import os

if os.name == 'nt':
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

import settings
from AI_agent import AI

game_board = tk.Tk()
game_board.title("Tic Tac Toc")
game_turn = 0
winner = False
symbol = [('X', '#BF3EFF'), ('O', '#FF8C00')]
player = []
ai_pos = None
human_pos = None
theme = None
ai = None

if os.name == 'nt':
    ai_image = ImageTk.PhotoImage(Image.open('./img/robot.png').resize((60, 70)))
    human_image = ImageTk.PhotoImage(Image.open('./img/child.png').resize((55, 65)))
else:
    ai_image = ImageTk.PhotoImage(Image.open('./img/robot.png').resize((35, 40)))
    human_image = ImageTk.PhotoImage(Image.open('./img/child.png').resize((30, 40)))


# game terminate state, win/loss/tie
def game_terminate(btn1, btn2, btn3):
    for i in range(9):
        settings.grids[i].config(state="disabled", cursor="")
        if i in [btn1, btn2, btn3]:
            settings.grids[i].config(bg="lightgreen", highlightbackground="lightgreen")

    game_board.update()

    if winner:
        settings.game_winner = player[(game_turn + 1) % 2]
        ai.check_and_learn()
        mg.showinfo("Game Settled", player[(game_turn + 1) % 2] + " WIN ! ")
    else:
        settings.game_winner = "DRAW"
        ai.check_and_learn()
        mg.showinfo("Game Settled", "DRAW ! ")

    # check if a winner exist


def check_win():
    global winner
    # check row & column
    for i in range(3):
        # check row
        if settings.grids[0 + i * 3]["text"] != " " and settings.grids[0 + i * 3]["text"] == settings.grids[1 + i * 3][
            "text"] == \
                settings.grids[2 + i * 3][
                    "text"]:
            winner = True
            game_terminate(0 + i * 3, 1 + i * 3, 2 + i * 3)
            return
        # check col
        elif settings.grids[0 + i]["text"] != " " and settings.grids[0 + i]["text"] == settings.grids[3 + i]["text"] == \
                settings.grids[6 + i]["text"]:
            winner = True
            game_terminate(0 + i, 3 + i, 6 + i)
            return
        # check diagonal
        elif settings.grids[4]["text"] != " " and settings.grids[0]["text"] == settings.grids[4]["text"] == \
                settings.grids[8]["text"]:
            winner = True
            game_terminate(0, 4, 8)
            return
        elif settings.grids[4]["text"] != " " and settings.grids[2]["text"] == settings.grids[4]["text"] == \
                settings.grids[6]["text"]:
            winner = True
            game_terminate(2, 4, 6)
            return

    # check tie
    if not winner and game_turn == 9:
        winner = False
        game_terminate(-1, -1, -1)
        return


# event when a button clicked
def button_clicked(but_num):
    global game_turn
    if settings.grids[but_num]["text"] == " ":
        settings.grids[but_num].config(text=symbol[game_turn % 2][0], state="disabled", cursor="",
                                       disabledforeground=symbol[game_turn % 2][1])
        game_turn += 1
        settings.play_history.append(but_num)
        settings.last_play = player[game_turn % 2]
        settings.board[but_num] = 1
        check_win()
        settings.ai_turn = not settings.ai_turn
        if settings.ai_turn and settings.game_winner is None:
            ai.draw()


# Initialize list of buttons
def init_button():
    for i in range(9):
        settings.grids.append(
            tk.Button(game_board, text=" ", font=("Helvetica", 25), height=3, width=6, bg="silver",
                      highlightbackground="silver", cursor="hand2",
                      disabledforeground="black", command=lambda but_num=i: button_clicked(but_num)))
        settings.grids[i].grid(row=(i + 3) // 3, column=i % 3)


# Reset all the button
def reset(ans):
    global game_turn, winner, ai
    for i in range(9):
        settings.grids[i].config(text=" ", bg="silver", highlightbackground="silver", cursor="hand2", state="normal")
    game_turn = 0
    winner = False
    settings.reset()
    del ai
    ai = AI()
    play_order(ans)


# decide the game order and display the img
def play_order(ans=None):
    global player, theme, ai_pos, human_pos
    if ans is None:
        ans = mg.askyesno("Question", "Do you want to play first?")
    if ans:
        player = ["YOU", "AI"]
    else:
        player = ["AI", "YOU"]
        settings.ai_turn = True
        ai.draw()

    if not theme:
        theme = tk.Frame(game_board)
        theme.grid(row=0, column=0, columnspan=3)
        ai_pos = tk.Label(theme, image=ai_image)
        ai_pos.grid(row=0, column=player.index('AI') * 2, padx=(player.index('AI') * 65, 0))
        tk.Label(theme, text=": X", font=("Helvetica", 25), height=1, fg='#BF3EFF').grid(row=0, column=1)
        human_pos = tk.Label(theme, image=human_image)
        human_pos.grid(row=0, column=player.index('YOU') * 2, padx=(player.index('YOU') * 65, 0))
        tk.Label(theme, text=": O", font=("Helvetica", 25), height=1, fg='#FF8C00').grid(row=0, column=3)
    else:
        ai_pos.grid(row=0, column=player.index('AI') * 2, padx=(player.index('AI') * 55, 0))
        human_pos.grid(row=0, column=player.index('YOU') * 2, padx=(player.index('YOU') * 55, 0))


# create user menu
def init_menu():
    top_bar = tk.Menu(game_board)
    menu = tk.Menu(top_bar, tearoff=False)
    menu.add_command(label="Reset as 1st", command=lambda: reset(1))
    menu.add_command(label="Reset as 2nd", command=lambda: reset(0))
    menu.add_command(label="Exit", command=lambda: exit(0))
    top_bar.add_cascade(label="Select", menu=menu)
    # topBar.add_command(label="RESET", command=lambda: reset())
    game_board.config(menu=top_bar)


def init():
    global ai
    ai = AI()
    init_menu()
    init_button()
    game_board.eval('tk::PlaceWindow . center')
    play_order()
    game_board.mainloop()
