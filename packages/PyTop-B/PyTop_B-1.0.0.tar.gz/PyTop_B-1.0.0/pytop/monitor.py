import curses
import psutil 

class PyTop:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.curs_set(0)  # Hide cursor
        self.stdscr.timeout(1000)  # Update every 1 second
        self.stdscr.keypad(True)
        self.running = True

    def display_header(self):
        self.stdscr.addstr(0, 0, "PID\tUSER\tCPU%\tMEM%\tCOMMAND", curses.A_BOLD)

    def display_process(self, process, row):
        try:
            user = process.username()
            cpu_percent = process.cpu_percent()
            mem_percent = process.memory_percent()
            command = " ".join(process.cmdline())
            if len(command) > curses.COLS - 40:  # Adjust for the width of other columns
                command = command[:curses.COLS - 40 - 3] + "..."  # Truncate long commands
            self.stdscr.addstr(row, 0, f"{process.pid}\t{user}\t{cpu_percent:.2f}\t{mem_percent:.2f}\t{command}")
            if cpu_percent > 50:
                self.stdscr.addstr(row, 20, f"{cpu_percent:.2f}%", curses.color_pair(2))
            else:
                self.stdscr.addstr(row, 20, f"{cpu_percent:.2f}%", curses.color_pair(1))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    def display_footer(self):
        self.stdscr.addstr(curses.LINES - 1, 0, "Press 'q' to quit")

    def run(self):
        while self.running:
            self.stdscr.clear()
            self.display_header()
            processes = sorted(psutil.process_iter(), key=lambda p: p.cpu_percent(), reverse=True)
            for i, process in enumerate(processes[:curses.LINES - 2]):  # Limit displayed processes to screen size
                self.display_process(process, i + 1)
            self.display_footer()
            self.stdscr.refresh()
            c = self.stdscr.getch()
            if c == ord('q'):
                self.running = False

    def cleanup(self):
        curses.curs_set(1)  # Restore cursor visibility
        curses.endwin()
 