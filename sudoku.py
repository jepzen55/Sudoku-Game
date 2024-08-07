import numpy as np
import random
import tkinter as tk
from tkinter import messagebox

def create_empty_board():
    return np.zeros((9, 9), dtype=int)

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row, col] = num
                        if solve_sudoku(board):
                            return True
                        board[row, col] = 0
                return False
    return True

def generate_sudoku():
    board = create_empty_board()
    solve_sudoku(board)
    return board

def remove_numbers(board, difficulty):
    if difficulty == 'easy':
        attempts = 40
    elif difficulty == 'hard':
        attempts = 50
    elif difficulty == 'extreme':
        attempts = 60
    else:
        raise ValueError("Invalid difficulty level")

    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row, col] != 0:
            backup = board[row, col]
            board[row, col] = 0

            copy_board = board.copy()
            if not solve_sudoku(copy_board):
                board[row, col] = backup
            else:
                attempts -= 1
    return board

class SudokuGUI:
    def __init__(self, root, difficulty='easy'):
        self.root = root
        self.difficulty = difficulty
        self.board = generate_sudoku()
        self.board = remove_numbers(self.board, difficulty)
        self.solution = self.board.copy()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_board()

    def create_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row, col] != 0:
                    cell = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center', fg='blue')
                    cell.insert(0, str(self.board[row, col]))
                    cell.config(state='readonly')
                else:
                    cell = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                    cell.bind('<FocusOut>', self.validate)
                cell.grid(row=row, column=col)
                self.cells[row][col] = cell

    def validate(self, event):
        for row in range(9):
            for col in range(9):
                cell_value = self.cells[row][col].get()
                if cell_value:
                    try:
                        value = int(cell_value)
                        if value < 1 or value > 9 or not is_valid(self.board, row, col, value):
                            self.cells[row][col].delete(0, tk.END)
                    except ValueError:
                        messagebox.showerror("Invalid Entry", "Please enter a valid number (1-9).")
                        self.cells[row][col].delete(0, tk.END)

    def check_solution(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].get() == "":
                    return False
                if int(self.cells[row][col].get()) != self.solution[row, col]:
                    return False
        return True

    def show_solution(self):
        if self.check_solution():
            messagebox.showinfo("Congratulations", "You solved the Sudoku!")
        else:
            messagebox.showinfo("Incorrect", "The solution is not correct. Keep trying!")

def new_game(difficulty):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.destroy()
    game = SudokuGUI(root, difficulty)
    check_button = tk.Button(root, text="Check Solution", command=game.show_solution)
    check_button.grid(row=10, columnspan=9)

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root)
    check_button = tk.Button(root, text="Check Solution", command=game.show_solution)
    check_button.grid(row=10, columnspan=9)
    
    difficulty_frame = tk.Frame(root)
    difficulty_frame.grid(row=11, columnspan=9)
    
    tk.Label(difficulty_frame, text="Select Difficulty:").pack(side=tk.LEFT)
    difficulties = ['easy', 'hard', 'extreme']
    selected_difficulty = tk.StringVar(value='easy')
    for difficulty in difficulties:
        tk.Radiobutton(difficulty_frame, text=difficulty.capitalize(), variable=selected_difficulty, value=difficulty).pack(side=tk.LEFT)
    
    newgame_button = tk.Button(root, text="New Game", command=lambda: new_game(selected_difficulty.get()))
    newgame_button.grid(row=12, columnspan=9)
    
    root.mainloop()
