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


        
