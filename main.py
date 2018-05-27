import curses
from curses.textpad import Textbox, rectangle
import threading
import time

NUM_LINES = 1
NUM_COLS = 80
PADDING = 2
options = ["▼ GET"]

def setup_brand(stdscr):
    height,width = stdscr.getmaxyx()

    if height<50 or width<75:
        return

    TOP = height//8
    LEFT = width//10

    P_START_INDEX = 0
    P_END_INDEX = 4
    O_START_INDEX = 6
    O_END_INDEX = 10
    S_START_INDEX = 12
    S_END_INDEX = 16
    T_START_INDEX = 18
    T_END_INDEX = 22
    E_START_INDEX = 24
    E_END_INDEX = 28
    R_START_INDEX = 30
    R_END_INDEX = 34


    # Designing P
    for i in range(1, TOP):
        stdscr.chgat(i,LEFT+P_START_INDEX, 1, curses.A_REVERSE)

    for i in range(1,4):
        stdscr.chgat(1, LEFT + i, 1, curses.A_REVERSE)
        stdscr.chgat(3, LEFT + i, 1, curses.A_REVERSE)

    for i in range(1, 4):
        stdscr.chgat(i,LEFT+P_END_INDEX, 1, curses.A_REVERSE)


    #Designing O
    for i in range(1,TOP):
        stdscr.chgat(i,LEFT+O_START_INDEX,1,curses.A_REVERSE)

    for i in range(1,O_END_INDEX-O_START_INDEX):
        stdscr.chgat(1,LEFT+O_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(TOP-1,LEFT+O_START_INDEX+i,1,curses.A_REVERSE)

    for i in range(1,TOP):
        stdscr.chgat(i,LEFT+O_END_INDEX,1,curses.A_REVERSE)


    #Designing S
    for i in range(1,TOP//2+1):
        stdscr.chgat(i,LEFT+S_START_INDEX,1,curses.A_REVERSE)

    for i in range(TOP//2+2,TOP):
        stdscr.chgat(i,LEFT+S_START_INDEX,1,curses.A_REVERSE)

    for i in range(1,S_END_INDEX-S_START_INDEX):
        stdscr.chgat(1,LEFT+S_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(3,LEFT+S_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(5,LEFT+S_START_INDEX+i,1,curses.A_REVERSE)

    stdscr.chgat(1, LEFT + S_END_INDEX, 1, curses.A_REVERSE)
    for i in range(TOP//2,TOP):
        stdscr.chgat(i,LEFT+S_END_INDEX,1,curses.A_REVERSE)

    #Designing T
    for i in range(T_END_INDEX-T_START_INDEX+1):
        stdscr.chgat(1,LEFT+T_START_INDEX+i,1,curses.A_REVERSE)

    for i in range(1,TOP):
        stdscr.chgat(i,LEFT+T_START_INDEX+(T_END_INDEX-T_START_INDEX)//2,1,curses.A_REVERSE)


    #Designing E
    for i in range(1,TOP):
        stdscr.chgat(i,LEFT+E_START_INDEX,1,curses.A_REVERSE)

    for i in range(1,E_END_INDEX-E_START_INDEX+1):
        stdscr.chgat(1,LEFT+E_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(3,LEFT+E_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(5,LEFT+E_START_INDEX+i,1,curses.A_REVERSE)


    # Designing R
    for i in range(1,R_END_INDEX-R_START_INDEX):
        stdscr.chgat(1,LEFT+R_START_INDEX+i,1,curses.A_REVERSE)
        stdscr.chgat(3,LEFT+R_START_INDEX+i,1,curses.A_REVERSE)

    for i in range(1,TOP):
        stdscr.chgat(i,LEFT+R_START_INDEX,1,curses.A_REVERSE)


    stdscr.chgat(4,LEFT+R_START_INDEX+1,1,curses.A_REVERSE)
    stdscr.chgat(TOP-1,LEFT+R_END_INDEX,1,curses.A_REVERSE)


    for i in range(1,4):
        stdscr.chgat(i, LEFT+R_END_INDEX, 1, curses.A_REVERSE)

def draw_menu(stdscr):
    chosen_option = options[0]
    height,width = stdscr.getmaxyx()

    setup_brand(stdscr)

    TOP = height//5
    LEFT = width//10

    stdscr.addstr(TOP,LEFT, chosen_option)

    #NEED TO USE getstr instead in order to keep track of the cursorcd 

    editwin = curses.newwin(NUM_LINES,NUM_COLS-1,TOP,LEFT+len(chosen_option)+2)
    rectangle(stdscr,TOP-PADDING,LEFT-PADDING,TOP+PADDING,LEFT+len(chosen_option)+NUM_COLS+PADDING)
    stdscr.refresh()
    box = Textbox(editwin)
    # Let the user edit until Ctrl-G is struck.
    box.edit()
    title = box.gather()[:-1]
    stdscr.clear()
    k = 0
    while k!=ord('q'):
        height,width = stdscr.getmaxyx()
        title = title[:width - 1]
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        stdscr.addstr(height//2, start_x_title, title)
        stdscr.refresh()
        k=stdscr.getch()

def main():
    curses.wrapper(draw_menu)
    

if __name__ == "__main__":
    main()