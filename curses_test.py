import time
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

file = open("podcast_list.txt", "r")

y = 0
names = []
links = []
for line in file:
	names.append(line.split(",")[0])
	links.append(line.split(",")[1])
	
podcasts = dict.fromkeys(names, links)

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

print(names)
print(links)
