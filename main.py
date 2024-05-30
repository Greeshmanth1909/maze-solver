from graphics import Window

def main():
    win = Window(800, 600)
    win.draw_line(500, 150, 600, 150)
    win.draw_line(500, 150, 500, 500)
    win.wait_for_close()


main()
