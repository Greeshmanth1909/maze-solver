from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title("Maze Solver")
        self.canvas = Canvas()
        self.canvas.pack()
        self.is_window_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_window_running = True
        while self.is_window_running:
            self.redraw()
        
    def close(self):
        self.is_window_running = False


def main():
    win = Window(800, 600)
    win.wait_for_close()
        
