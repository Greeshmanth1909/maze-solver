from tkinter import Tk, BOTH, Canvas
import time, random

class Window():

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.__root.title("Maze Solver")
        self.__root.configure(bg="white")
        self.canvas = Canvas()
        self.canvas.configure(bg="#d9d9d9")
        self.canvas.pack(fill=BOTH, expand=1)
        self.is_window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_window_running = True
        while self.is_window_running:
            self.redraw()
        
    def close(self):
        self.is_window_running = False

    def draw_line(self, x1, y1, x2, y2, color):
        line = Line(x1, y1, x2, y2)
        line.draw(self.canvas, color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)

class Cell():
    def __init__(self, left_wall, right_wall, top_wall, bottom_wall, x1, y1, x2, y2, win):
        self.left_wall = left_wall
        self.right_wall = right_wall
        self.top_wall = top_wall
        self.bottom_wall = bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self._visited = False

    def draw(self):
        if self.left_wall:
            self._win.draw_line(self._x1, self._y1, self._x1, self._y2, "black")
        else:
            self._win.draw_line(self._x1, self._y1, self._x1, self._y2, "#d9d9d9")

        if self.right_wall:
            self._win.draw_line(self._x2, self._y1, self._x2, self._y2, "black")
        else:
            self._win.draw_line(self._x2, self._y1, self._x2, self._y2, "#d9d9d9")

        if self.top_wall:
            self._win.draw_line(self._x1, self._y1, self._x2, self._y1, "black")
        else:
            self._win.draw_line(self._x1, self._y1, self._x2, self._y1, "#d9d9d9")

        if self.bottom_wall:
            self._win.draw_line(self._x1, self._y2, self._x2, self._y2, "black")
        else:
            self._win.draw_line(self._x1, self._y2, self._x2, self._y2, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        from_center_x = (self._x1 + self._x2) / 2
        from_center_y = (self._y1 + self._y2) / 2
        to_center_x = (to_cell._x1 + to_cell._x2) / 2
        to_center_y = (to_cell._y1 + to_cell._y2) / 2
        if undo:
            self._win.draw_line(from_center_x, from_center_y, to_center_x, to_center_y, "gray")
        else:
            self._win.draw_line(from_center_x, from_center_y, to_center_x, to_center_y, "red")

class Maze():

    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self.visited_set = set()
        self._create_cells()
        

    def _create_cells(self):
        row_x = self._x1
        row_y = self._y1
        for i in range(self._num_cols):
            current_row = []
            row_y += self._cell_size_y
            for j in range(self._num_rows):
                x1 = row_x + j * self._cell_size_x
                y1 = row_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                current_row.append(Cell(True, True, True, True, x1, y1, x2, y2, self._win))
            self._cells.append(current_row)

        # matrix is populated with cell objects call _draw for each of them
        for row in self._cells:
            for cell in row:
                self._draw_cell(cell)

        self._break_entrance_and_exit()
        self._draw_cell(self._cells[0][0])
        self._draw_cell(self._cells[self._num_cols - 1][self._num_rows - 1])
        self._break_walls_r(0, 0)
        for row in self._cells:
            for cell in row:
                self._draw_cell(cell)


    def _draw_cell(self, cell):
        cell.draw()
        self._animate()


    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
         
    def _break_entrance_and_exit(self):
        # Break top of top left cell
        self._cells[0][0].top_wall = False

        # Break bottom wall of bottom left cell
        self._cells[self._num_cols - 1][self._num_rows - 1].bottom_wall = False


    def _break_walls_r(self, i, j):
        # i and j are indexes to the cell in self._cells list
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return
        

        visited = (i, j)
        self.visited_set.add(visited)
        valid_paths = self._possible_paths(i, j)

        # valid paths is a set of available options from the given cell, negate it with self.visited set
        #valid_paths = sorted(valid_paths.difference(self.visited_set))
        # choose from available paths
        random_choice = random.choice(sorted(valid_paths))
        valid_paths = list(valid_paths)
        random.shuffle(valid_paths)
        for path in valid_paths:
            if path not in self.visited_set:
                random_choice = path
        

            

        # break wall to that node
        # i represents the row and j represents the column
        cell_row = random_choice[0]
        cell_col = random_choice[1]
        next_cell = self._cells[cell_row][cell_col]
        current_cell = self._cells[i][j]
        if cell_row > i:
            # go to bottom cell
            current_cell.bottom_wall = False
            next_cell.top_wall = False

        elif cell_row < i:
            # go to top cell
            current_cell.top_wall = False
            next_cell.bottom_wall = False

        elif cell_col > j:
            # go to right cell
            current_cell.right_wall = False
            next_cell.left_wall = False

        elif cell_col < j:
            # go to left cell
            current_cell.left_wall = False
            next_cell.right_wall = False

        return self._break_walls_r(cell_row, cell_col)


    def _possible_paths(self, i, j):
        # for given cell index i, j provide a list of possible paths from it as a list of tuples [(i, j)]
        max_rows = self._num_cols - 1
        max_cols = self._num_rows - 1
        min_rows = 0
        min_cols = 0
        possible_paths_set = set()
        # if i and j are out of range, raise an error
        if i > max_rows or i < min_rows or j > max_cols or j < min_cols:
            raise Exception("Invalid Index provided for given maze")

        if i + 1 <= max_rows:
            possible_paths_set.add((i + 1, j))
        if i - 1 >= min_rows:
            possible_paths_set.add((i - 1, j))
        if j + 1 <= max_cols:
            possible_paths_set.add((i, j + 1))
        if j - 1 >= min_cols:
            possible_paths_set.add((i, j - 1))

        return possible_paths_set
