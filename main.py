from graphics import Window, Cell

def main():
    win = Window(800, 600)
    cell = Cell(True, True, False, True, 100, 250, 200, 350, win)
    cell1 = Cell(True, True, False, True, 300, 350, 400, 450, win)
    cell1.draw()

    cell.draw()
    win.wait_for_close()


main()
