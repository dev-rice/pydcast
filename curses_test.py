import time
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

while True:
    c = stdscr.getch()

    if c == curses.KEY_UP:
        stdscr.addstr("up")
    elif c == curses.KEY_DOWN:
        stdscr.addstr("down")
    elif c == ord('q'):
        break
    
    stdscr.refresh()

#Close Curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()