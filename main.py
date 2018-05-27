import curses
from curses.textpad import Textbox, rectangle
import string
import json
import requests

NUM_LINES = 1
NUM_COLS = 80
PADDING = 2
TOP,LEFT = 0,0
options = ["GET","POST","PATCH","DELETE"]
CTRL_X = 24
REQUEST_TITLE = "Request"
RESPONSE_TITLE = "Response"
ENTER = 10

global_stdscr = None
last_key_pressed = 0

chosen_option = "▼ "+options[0]
selected_option = 0

def setup_brand(stdscr):
    global global_stdscr
    global_stdscr = stdscr

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

box = None
edit_box_message = ""
INIT_CURSES = 0
edit_box_curses_x = 0
move_indexes = {"move_to_dropdown":1,"edit_message_box":2,"request":3,"toggle_dropdown":4,"click_request":5}
chosen_move_index = move_indexes["edit_message_box"]


def move_to_dropdown():
    global chosen_option,global_stdscr,chosen_move_index,last_key_pressed
    height,width = global_stdscr.getmaxyx()
    global_stdscr.chgat(height // 5,width//10,len(chosen_option),curses.A_REVERSE)
    last_key_pressed = global_stdscr.getch()
    if last_key_pressed == curses.KEY_RIGHT:
        chosen_move_index = move_indexes["edit_message_box"]
    elif last_key_pressed == ENTER:
        chosen_move_index = move_indexes["toggle_dropdown"]


def toggle_dropdown():
    global global_stdscr,options,last_key_pressed,selected_option,chosen_move_index,chosen_option
    rectangle(global_stdscr,TOP+3,LEFT-PADDING,TOP+len(options)*PADDING+1,LEFT+4*PADDING)
    unselected_options = [option for option in options if option!=chosen_option[2:]]
    for i,option in enumerate(unselected_options):
        global_stdscr.addstr(TOP+2+PADDING*(i+1),LEFT,option)
        if selected_option==i:
            global_stdscr.chgat(TOP+2+PADDING*(i+1),LEFT,len(option),curses.A_REVERSE)

    last_key_pressed = global_stdscr.getch()
    if last_key_pressed == curses.KEY_DOWN:
        selected_option +=1
        if selected_option>2:
            selected_option=2
    elif last_key_pressed == curses.KEY_UP:
        selected_option-=1
        if selected_option<0:
            selected_option=0
            chosen_move_index = move_indexes["move_to_dropdown"]
    elif last_key_pressed == ENTER:
        chosen_option = "▼ "+unselected_options[selected_option]
        selected_option = 0
        chosen_move_index = move_indexes["move_to_dropdown"]


def navigator(keystroke):
    global edit_box_message,INIT_CURSES,edit_box_curses_x,chosen_move_index,last_key_pressed
    if keystroke == CTRL_X:
        last_key_pressed = keystroke
        return 7

    if keystroke==curses.KEY_LEFT:
        if edit_box_curses_x==0:
            chosen_move_index = move_indexes["move_to_dropdown"]
            last_key_pressed = 7
            return 7
        edit_box_curses_x = edit_box_curses_x-1 if edit_box_curses_x>0 else 0

    if keystroke==curses.KEY_RIGHT:
        if len(edit_box_message)==edit_box_curses_x:
            chosen_move_index = move_indexes["request"]
            last_key_pressed = 7
            return  7
        edit_box_curses_x = edit_box_curses_x+1 if edit_box_curses_x<INIT_CURSES+NUM_COLS else INIT_CURSES+NUM_COLS

    if keystroke==curses.KEY_BACKSPACE:
        edit_box_message = edit_box_message[:-1]
        edit_box_curses_x-=1
        if len(edit_box_message)==0:
            edit_box_curses_x=0

    if chr(keystroke).lower() in string.ascii_lowercase or chr(keystroke) in ["/", ":", "."]:
        edit_box_message+=chr(keystroke)
        edit_box_curses_x+=1
    last_key_pressed = keystroke
    return keystroke


response_data = None
response_data_url = None
response_data_cursor_x = 0
def format_data(response_data, height):
    global response_data_cursor_x
    for i in range(height-3):
        if i<len(response_data):
            global_stdscr.addstr(3+i, LEFT + len(chosen_option) + len(REQUEST_TITLE) + NUM_COLS + 4 * PADDING + 2,response_data[i])
            if i==response_data_cursor_x:
                global_stdscr.chgat(3+i,LEFT + len(chosen_option) + len(REQUEST_TITLE) + NUM_COLS + 4 * PADDING + 2,len(response_data[i]),curses.A_REVERSE)


def click_request():
    global response_data,last_key_pressed,edit_box_message,response_data_cursor_x,chosen_move_index,response_data_url
    # populate response div
    height,width = global_stdscr.getmaxyx()
    if not response_data or (response_data!=None and edit_box_message!=response_data_url):
        try:
            chosen_option_stripped = chosen_option[2:]
            if chosen_option_stripped == "GET":
                response_data = json.dumps(requests.get(edit_box_message).json(),indent=1,sort_keys=True).split("\n")
            # elif chosen_option_stripped == "POST":
            #     response_data = json.dumps(requests.get(edit_box_message).json(),indent=1,sort_keys=True).split("\n")
            # elif chosen_option_stripped == "PATCH":
            #     response_data = json.dumps(requests.get(edit_box_message).json(),indent=1,sort_keys=True).split("\n")
            # elif chosen_option_stripped == "DELETE":
            #     response_data = json.dumps(requests.get(edit_box_message).json(),indent=1,sort_keys=True).split("\n")
            format_data(response_data, height)
        except:
            format_data(["There was an error processing the url..."],height)
    else:
        format_data(response_data, height)

    response_data_url = edit_box_message
    last_key_pressed = global_stdscr.getch()
    if last_key_pressed == curses.KEY_LEFT:
        chosen_move_index = move_indexes["request"]
    elif last_key_pressed == curses.KEY_DOWN:
        response_data_cursor_x +=1
        if response_data_cursor_x>height-3:
            response_data_cursor_x = height - 3
        elif response_data_cursor_x>len(response_data)-1:
            response_data_cursor_x = len(response_data)-1
    elif last_key_pressed == curses.KEY_UP:
        response_data_cursor_x -=1
        if response_data_cursor_x < 0 :
            response_data_cursor_x=0


def request():
    global edit_box_message,last_key_pressed,chosen_move_index
    global_stdscr.chgat(TOP, LEFT + len(chosen_option) + NUM_COLS + 2*PADDING+1,len(REQUEST_TITLE),curses.A_REVERSE)
    last_key_pressed = global_stdscr.getch()
    if last_key_pressed == curses.KEY_LEFT:
        chosen_move_index = move_indexes["edit_message_box"]
    elif last_key_pressed == ENTER:
        chosen_move_index = move_indexes["click_request"]


def edit_box():
    global box,NUM_LINES,NUM_COLS,TOP,LEFT,chosen_option,edit_box_curses_x,edit_box_message
    if len(edit_box_message)!=0:
        edit_box_curses_x=len(edit_box_message)
    editwin = curses.newwin(NUM_LINES, NUM_COLS - 1, TOP, LEFT + len(chosen_option) + 2)
    box = Textbox(editwin)
    for char in edit_box_message:
        box.do_command(char)
    box.edit(navigator)


def setup():
    global last_key_pressed,box,INIT_CURSES,global_stdscr,chosen_option,TOP,LEFT,chosen_move_index,edit_box_message

    while last_key_pressed!=CTRL_X:
        global_stdscr.clear()
        height, width = global_stdscr.getmaxyx()
        TOP = height // 5
        LEFT = width // 10

        setup_brand(global_stdscr)
        INIT_CURSES = LEFT + len(chosen_option) + 2

        #options
        global_stdscr.addstr(TOP, LEFT, chosen_option)

        #editbox
        rectangle(global_stdscr, TOP - PADDING, LEFT - PADDING, TOP + PADDING, LEFT + len(chosen_option) + NUM_COLS + PADDING)
        global_stdscr.addstr(TOP, LEFT + len(chosen_option) + 2,edit_box_message)

        #request button
        global_stdscr.addstr(TOP, LEFT + len(chosen_option) + 2*PADDING +1 + NUM_COLS,REQUEST_TITLE)
        rectangle(global_stdscr, TOP - PADDING, LEFT + len(chosen_option) + NUM_COLS + 2*PADDING, TOP + PADDING, LEFT + len(chosen_option)+len(REQUEST_TITLE) + NUM_COLS + 2*PADDING+1)

        #response div
        global_stdscr.addstr(1, LEFT + len(chosen_option)+len(REQUEST_TITLE) + NUM_COLS + 4*PADDING+1,RESPONSE_TITLE)
        rectangle(global_stdscr,2, LEFT + len(chosen_option)+len(REQUEST_TITLE) + NUM_COLS + 4*PADDING+1,height-2,width-2)

        global_stdscr.refresh()
        curses.curs_set(False)
        if chosen_move_index == move_indexes["move_to_dropdown"]:
            move_to_dropdown()
        elif chosen_move_index == move_indexes["request"]:
            request()
        elif chosen_move_index == move_indexes["edit_message_box"]:
            curses.curs_set(True)
            edit_box()
        elif chosen_move_index == move_indexes["toggle_dropdown"]:
            toggle_dropdown()
        elif chosen_move_index == move_indexes["click_request"]:
            click_request()


def draw_menu(stdscr):
    global global_stdscr
    global_stdscr = stdscr
    setup()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()