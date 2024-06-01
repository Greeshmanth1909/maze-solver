from tkinter import Tk, BOTH, Canvas
import time

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
