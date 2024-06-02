from graphics import Window, Cell, Maze

def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 9, 9, 60, 40, win) 
    win.wait_for_close()
main()
