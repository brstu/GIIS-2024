import secrets
import tkinter as tk

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.focus_set()
        self.master.bind("<Key>", self.key_pressed)
        self.commands = {'W': 'up', 'S': 'down', 'A': 'left', 'D': 'right'}
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.mainloop()

    def init_grid(self):
        background = tk.Frame(self, bg="#92877d", width=400, height=400)
        background.grid()
        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(background, bg="#9e948a", width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text="", bg="#9e948a", justify=tk.CENTER, font=("Helvetica", 36, "bold"), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            row, col = secrets.choice(empty_cells)
            self.matrix[row][col] = secrets.choice([2, 4])

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.matrix[i][j]
                cell = self.grid_cells[i][j]
                if new_number == 0:
                    cell.configure(text="", bg="#9e948a")
                else:
                    cell.configure(text=str(new_number), bg=self.get_color(new_number))

    def get_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#ff0000")

    def key_pressed(self, event):
        key = event.keysym.upper()
        if key in self.commands:
            new_matrix, changed, _ = getattr(self, self.commands[key])(self.matrix)
            if changed:
                self.matrix = new_matrix
                self.add_new_tile()
                self.update_grid_cells()

    def left(self, matrix):
        new_matrix = []
        score = 0
        for row in matrix:
            new_row, row_score = self.compress(row)
            new_matrix.append(new_row)
            score += row_score
        return new_matrix, matrix != new_matrix, score

    def right(self, matrix):
        new_matrix = []
        score = 0
        for row in matrix:
            new_row, row_score = self.compress(row[::-1])
            new_matrix.append(new_row[::-1])
            score += row_score
        return new_matrix, matrix != new_matrix, score

    def up(self, matrix):
        new_matrix = [[0] * 4 for _ in range(4)]
        score = 0
        for col in range(4):
            column = [matrix[row][col] for row in range(4)]
            new_col, col_score = self.compress(column)
            for row in range(4):
                new_matrix[row][col] = new_col[row]
            score += col_score
        return new_matrix, matrix != new_matrix, score

    def down(self, matrix):
        new_matrix = [[0] * 4 for _ in range(4)]
        score = 0
        for col in range(4):
            column = [matrix[row][col] for row in range(4)]
            new_col, col_score = self.compress(column[::-1])
            for row in range(4):
                new_matrix[row][col] = new_col[::-1][row]
            score += col_score
        return new_matrix, matrix != new_matrix, score

    def compress(self, line):
        new_line = [i for i in line if i != 0]
        while len(new_line) < 4:
            new_line.append(0)
        score = 0
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1] and new_line[i] != 0:
                new_line[i] *= 2
                score += new_line[i]
                new_line[i + 1] = 0
        new_line = [i for i in new_line if i != 0]
        while len(new_line) < 4:
            new_line.append(0)
        return new_line, score


game = Game2048()