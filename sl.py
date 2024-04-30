import curses
import signal
import time

# Define constants
LOGO_HEIGHT = 6
LOGO_FUNNEL = 4
LOGO_LENGTH = 84
LOGO_PATTERNS = 6

D51_HEIGHT = 10
D51_FUNNEL = 7
D51_LENGTH = 83
D51_PATTERNS = 6

C51_HEIGHT = 11
C51_FUNNEL = 7
C51_LENGTH = 87
C51_PATTERNS = 6

COLS = curses.COLS
LINES = curses.LINES

# Logo patterns
LOGO1 = "     ++      +------ "
LOGO2 = "     ||      |+-+ |  "
LOGO3 = "   /---------|| | |  "
LOGO4 = "  + ========  +-+ |  "

LWHL11 = " _|--O========O~\\-+  "
LWHL12 = "//// \\_/      \\_/    "

LWHL21 = " _|--/O========O\\-+  "
LWHL22 = "//// \\_/      \\_/    "

LWHL31 = " _|--/~O========O-+  "
LWHL32 = "//// \\_/      \\_/    "

LWHL41 = " _|--/~\\------/~\\-+  "
LWHL42 = "//// \\_O========O    "

LWHL51 = " _|--/~\\------/~\\-+  "
LWHL52 = "//// \\O========O/    "

LWHL61 = " _|--/~\\------/~\\-+  "
LWHL62 = "//// O========O_/    "

LCOAL1 = "____                 "
LCOAL2 = "|   \\@@@@@@@@@@@     "
LCOAL3 = "|    \\@@@@@@@@@@@@@_ "
LCOAL4 = "|                  | "
LCOAL5 = "|__________________| "
LCOAL6 = "   (O)       (O)     "

LCAR1 = "____________________ "
LCAR2 = "|  ___ ___ ___ ___ | "
LCAR3 = "|  |_| |_| |_| |_| | "
LCAR4 = "|__________________| "
LCAR5 = "|__________________| "
LCAR6 = "   (O)        (O)    "

LOGO_HEIGHTS = [LOGO1, LOGO2, LOGO3, LOGO4, LWHL11, LWHL12]
LCOAL_HEIGHTS = [LCOAL1, LCOAL2, LCOAL3, LCOAL4, LCOAL5, LCOAL6]
LCAR_HEIGHTS = [LCAR1, LCAR2, LCAR3, LCAR4, LCAR5, LCAR6]

# Define signal handler
def signal_handler(signal, frame):
    curses.endwin()
    exit(0)

# Add smoke to the screen
def add_smoke(window, y, x, smoke_pattern):
    smoke_patterns = [
        ["(   )", "(    )", "(    )", "(   )", "(  )", "(  )", "( )", "( )", "()", "()", "O"],
        ["(@@@)", "(@@@@)", "(@@@@)", "(@@@)", "(@@)", "(@@)", "(@)", "(@)", "@@", "@@", "@", "@"]
    ]
    erase_pattern = [" " * len(s) for s in smoke_pattern]
    dy = [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    dx = [-2, -1, 0, 1, 1, 1, 1, 1, 2, 2, 3]

    if x % 4 == 0:
        for i, s in enumerate(smoke_patterns[smoke_pattern % 2]):
            window.addstr(y + i, x, erase_pattern[i])
            y -= dy[i]
            x += dx[i]
            window.addstr(y, x, s)
        smoke_pattern += 1

    return smoke_pattern

# Add man to the screen
def add_man(window, y, x):
    man = ["", "(O)", "Help!", "\\O/"]
    for i, m in enumerate(man):
        window.addstr(y + i, x, m)

# Add vehicle to the screen
def add_vehicle(window, y, x, logo=True, vehicle_type="D51", fly=False, accident=False):
    logo_patterns = [
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL11, LWHL12],
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL21, LWHL22],
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL31, LWHL32],
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL41, LWHL42],
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL51, LWHL52],
        [LOGO1, LOGO2, LOGO3, LOGO4, LWHL61, LWHL62]
    ]
    coal_heights = LCOAL_HEIGHTS
    car_heights = LCAR_HEIGHTS

    vehicle_heights = logo_patterns if logo else car_heights if vehicle_type == "C51" else coal_heights

    for i, vh in enumerate(vehicle_heights):
        window.addstr(y + i, x, vh)

    if accident:
        add_man(window, y + 1, x + 14)
        if vehicle_type == "C51":
            add_man(window, y + 1, x + 45)
            add_man(window, y + 1, x + 53)
            add_man(window, y + 1, x + 66)
            add_man(window, y + 1, x + 74)
        else:
            add_man(window, y + 2, x + 43)
            add_man(window, y + 2, x + 47)

# Main function
def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.scrollok(False)

    x = curses.COLS - 1
    logo = 1
    fly = 0
    C51 = 0
    ACCIDENT = 0

    while True:
        if logo:
            if add_vehicle(stdscr, LINES // 2 - 3, x, logo=True, fly=fly, accident=ACCIDENT) == curses.ERR:
                break
        elif C51:
            if add_vehicle(stdscr, LINES // 2 - 5, x, logo=False, vehicle_type="C51", fly=fly, accident=ACCIDENT) == curses.ERR:
                break
        else:
            if add_vehicle(stdscr, LINES // 2 - 4, x, logo=False, vehicle_type="D51", fly=fly, accident=ACCIDENT) == curses.ERR:
                break

        if fly:
            y = (LINES - LOGO_HEIGHT - 1) // 2 - 5 + 1
            x += 1
            stdscr.refresh()
            time.sleep(0.1)

            if x > curses.COLS - 2:
                x = curses.COLS - 1
                fly = 0
        else:
            x -= 1
            if x < 0:
                x = curses.COLS - 1
                fly = 1
                if logo:
                    logo = 0
                else:
                    if C51:
                        C51 = 0
                    else:
                        C51 = 1

        if ACCIDENT:
            if x % 50 == 0:
                ACCIDENT = 0
        else:
            if x % 180 == 0:
                ACCIDENT = 1

        if stdscr.getch() == ord('q'):
            break

        curses.flushinp()

curses.wrapper(main)
