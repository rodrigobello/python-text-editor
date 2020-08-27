#!/usr/bin/env python3
import sys, tty, termios
from buffer import Buffer
from cursor import Cursor
from ansi import ANSI


class Editor:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, "r") as fp:
            lines = [line.replace("\n", "") for line in fp.readlines()]
        self.buffer = Buffer(lines)
        self.cursor = Cursor()
        self.history = []

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                self.render()
                self.handle_input()
        except Exception as e:
            print("\n" * 50)
            raise e
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def render(self):
        ANSI.clear_screen()
        ANSI.move_cursor(0, 0)
        self.buffer.render()
        ANSI.move_cursor(self.cursor.row, self.cursor.col)

    def handle_input(self):
        # ASCII TABLE: http://www.physics.udel.edu/~watson/scen103/ascii.html
        ch = sys.stdin.read(1)
        if ch == chr(17):  # ctrl+q
            sys.exit(0)
        elif ch == chr(21):  # ctrl+u
            self.restore_snapshot()
        elif ch == chr(23):  # ctrl+w
            self.save_changes()
        elif ch == chr(16):  # ctrl+p
            self.cursor = self.cursor.up(self.buffer)
        elif ch == chr(14):  # ctrl+n
            self.cursor = self.cursor.down(self.buffer)
        elif ch == chr(2):  # ctrl+b
            self.cursor = self.cursor.left(self.buffer)
        elif ch == chr(6):  # ctrl+f
            self.cursor = self.cursor.right(self.buffer)
        elif ch == chr(13):  # enter
            self.save_snapshot()
            self.buffer = self.buffer.split_line(self.cursor.row, self.cursor.col)
            self.cursor = self.cursor.down(self.buffer).move_to_col(0)
        elif ch == chr(127):  # backspace
            if self.cursor.col > 0:
                self.save_snapshot()
                self.buffer = self.buffer.delete(self.cursor.row, self.cursor.col - 1)
                self.cursor = self.cursor.left(self.buffer)
        else:
            self.save_snapshot()
            self.buffer = self.buffer.insert(ch, self.cursor.row, self.cursor.col)
            self.cursor = self.cursor.right(self.buffer)

    def save_snapshot(self):
        self.history.append([self.buffer, self.cursor])

    def restore_snapshot(self):
        if self.history:
            self.buffer, self.cursor = self.history.pop()

    def save_changes(self):
        with open(self.filepath, "w") as fp:
            fp.writelines([line + "\n" for line in self.buffer.lines])


if __name__ == "__main__":
    editor = Editor("random.txt")
    editor.run()
