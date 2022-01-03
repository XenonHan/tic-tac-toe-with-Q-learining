"""
This is the tic tac toc game board
"""

import future.moves.tkinter as tk
import future.moves.tkinter.messagebox as mg

game_board = tk.Tk()
game_board.title("Tic Tac Toc")
game_turn = 0
winner = False
symbol = ['X', 'O']
player = []
grids = []


# game terminate state, win/loss/tie
def game_terminate(btn1, btn2, btn3):
    for i in range(9):
        grids[i].config(state="disabled", cursor="")
        if i in [btn1, btn2, btn3]:
            grids[i].config(bg="green")

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
        if grids[0 + i * 3]["text"] != " " and grids[0 + i * 3]["text"] == grids[1 + i * 3]["text"] == grids[2 + i * 3][
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
        button.config(text=symbol[game_turn % 2], state="disabled", cursor="")
        game_turn += 1
        check_win()


# reset the game board
def reset():
    print("rest called")


# Initialize list of buttons
def init_button():
    for i in range(9):
        grids.append(
            tk.Button(game_board, text=" ", font=("Helvetica", 20), height=3, width=6, bg="silver", cursor="hand2",
                      disabledforeground="black", command=lambda but_num=i: button_clicked(grids[but_num])))
        grids[i].grid(row=i // 3, column=i % 3)


# Reset all the button
def reset():
    global game_turn
    for i in range(9):
        grids[i].config(text=" ", font=("Helvetica", 20), height=3, width=6, bg="silver", cursor="hand2",
                        disabledforeground="black", command=lambda but_num=i: button_clicked(grids[but_num]),
                        state="normal")
    game_turn = 0


# init state of the game, prompt the game order
def init():
    global player
    ans = mg.askyesno("Question", "Do you want to play first?")
    if ans:
        player = ["YOU", "AI"]
    else:
        player = ["AI", "YOU"]


# user menu
topBar = tk.Menu(game_board, tearoff=False)
topBar.add_command(label="RESET", command=lambda: reset())
game_board.config(menu=topBar)

# init
# game_board.minsize(250, 200)
init_button()
init()
game_board.mainloop()
