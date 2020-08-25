#!/usr/bin/env python3
import sys, tty, termios


class Editor:
    def __init__(self):
        lines = [
            line.replace("\n", "")
            for line in open("random.txt").readlines()
        ]
        self.buffer = Buffer(lines)
        self.cursor = Cursor()

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                self.render()
                self.handle_input()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def render(self):
        ANSI.clear_screen()
        ANSI.move_cursor(0, 0)
        self.buffer.render()
        ANSI.move_cursor(self.cursor.row, self.cursor.col)

    def handle_input(self):
        ch = sys.stdin.read(1)
        if ch == chr(17): # ctrl+q
           sys.exit(0)
        if ch == 'k':
            self.cursor = self.cursor.up()
        if ch == 'j':
            self.cursor = self.cursor.down()
        if ch == 'h':
            self.cursor = self.cursor.left()
        if ch == 'l':
            self.cursor = self.cursor.right()


class ANSI:
    @classmethod
    def clear_screen(cls):
        print("[2J")

    @classmethod
    def move_cursor(cls, row, col):
        print(f"[{row + 1};{col + 1}H")


class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def render(self):
        for line in self.lines:
            print(line, end='\r\n')


class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def up(self):
        return Cursor(self.row - 1, self.col)

    def down(self):
        return Cursor(self.row + 1, self.col)

    def left(self):
        return Cursor(self.row, self.col - 1)

    def right(self):
        return Cursor(self.row, self.col + 1)


if __name__ == '__main__':
    editor = Editor()
    editor.run()
