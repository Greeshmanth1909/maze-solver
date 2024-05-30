from tkinter import Tk, BOTH, Canvas

class Window():

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.__root.title("Maze Solver")
        self.canvas = Canvas()
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

    def draw_line(self, x1, y1, x2, y2):
        line = Line(x1, y1, x2, y2)
        line.draw(self.canvas, "black")

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
            self._win.draw_line(self._x1, self._y1, self._x1, self._y2)
        if self.right_wall:
            self._win.draw_line(self._x2, self._y1, self._x2, self._y2)
        if self.top_wall:
            self._win.draw_line(self._x1, self._y1, self._x2, self._y1)
        if self.bottom_wall:
            self._win.draw_line(self._x1, self._y2, self._x2, self._y2)
 
