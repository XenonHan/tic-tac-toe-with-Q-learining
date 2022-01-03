"""
This is the tic tac toc game board
"""

import future.moves.tkinter as tk
import future.moves.tkinter.messagebox as mg
from PIL import Image, ImageTk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

game_board = tk.Tk()
game_board.title("Tic Tac Toc")
game_turn = 0
winner = False
symbol = [('X','#BF3EFF'), ('O','#FF8C00')]
player = []
grids = []
ai_pos = None
human_pos = None
theme = None
ai_image = ImageTk.PhotoImage(Image.open('./img/robot.png').resize((50, 60)))
human_image = ImageTk.PhotoImage(Image.open('./img/child.png').resize((45, 55)))


# game terminate state, win/loss/tie
def game_terminate(btn1, btn2, btn3):
    for i in range(9):
        grids[i].config(state="disabled", cursor="")
        if i in [btn1, btn2, btn3]:
            grids[i].config(bg="lightgreen")

    print(game_turn)
    if winner:
        mg.showinfo("Game Settled", player[(game_turn + 1) % 2] + " WIN ! ")
    else:
        mg.showinfo("Game Settled", "DRAW ! ")


# check if a winner exist
def check_win():
    global winner
    # check row & column
    for i in range(3):
        # check row
        if grids[0 + i * 3]["text"] != " " and grids[0 + i * 3]["text"] == grids[1 + i * 3]["text"] == \
                grids[2 + i * 3][
                    "text"]:
            winner = True
            game_terminate(0 + i * 3, 1 + i * 3, 2 + i * 3)
            return
        # check col
        elif grids[0 + i]["text"] != " " and grids[0 + i]["text"] == grids[3 + i]["text"] == grids[6 + i]["text"]:
            winner = True
            game_terminate(0 + i, 3 + i, 6 + i)
            return
        # check diagonal
        elif grids[4]["text"] != " " and grids[0]["text"] == grids[4]["text"] == grids[8]["text"]:
            winner = True
            game_terminate(0, 4, 8)
            return
        elif grids[4]["text"] != " " and grids[2]["text"] == grids[4]["text"] == grids[6]["text"]:
            winner = True
            game_terminate(2, 4, 6)
            return

    # check tie
    if not winner and game_turn == 9:
        winner = False
        game_terminate(-1, -1, -1)
        return


# event when a button clicked
def button_clicked(button):
    global game_turn
    if button["text"] == " ":
        button.config(text=symbol[game_turn % 2][0], state="disabled", cursor="", disabledforeground=symbol[game_turn % 2][1])
        game_turn += 1
        check_win()


# Initialize list of buttons
def init_button():
    for i in range(9):
        grids.append(
            tk.Button(game_board, text=" ", font=("Helvetica", 20), height=3, width=6, bg="silver", cursor="hand2",
                      disabledforeground="black", command=lambda but_num=i: button_clicked(grids[but_num])))
        grids[i].grid(row=(i + 3) // 3, column=i % 3)


# Reset all the button
def reset(ans):
    global game_turn, winner
    for i in range(9):
        grids[i].config(text=" ", bg="silver", cursor="hand2", state="normal")
    game_turn = 0
    winner = False
    play_order(ans)


# decide the game order and display the img
def play_order(ans=None):
    global player, theme, ai_pos, human_pos
    if ans is None:
        mg.askyesno("Question", "Do you want to play first?")
    if ans:
        player = ["YOU", "AI"]
    else:
        player = ["AI", "YOU"]

    if not theme:
        theme = tk.Frame(game_board)
        theme.grid(row=0, column=0, columnspan=3)
        ai_pos = tk.Label(theme, image=ai_image)
        ai_pos.grid(row=0, column=player.index('AI') * 2, padx=(player.index('AI') * 65, 0))
        tk.Label(theme, text=": X", font=("Helvetica", 20), height=1, fg='#BF3EFF').grid(row=0, column=1)
        human_pos = tk.Label(theme, image=human_image)
        human_pos.grid(row=0, column=player.index('YOU') * 2, padx=(player.index('YOU') * 65, 0))
        tk.Label(theme, text=": O", font=("Helvetica", 20), height=1, fg='#FF8C00').grid(row=0, column=3)
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


# init
init_menu()
init_button()
game_board.eval('tk::PlaceWindow . center')
play_order()
game_board.mainloop()
