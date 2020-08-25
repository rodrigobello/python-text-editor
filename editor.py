#!/usr/bin/env python3
import sys, tty, termios


class Editor:
    def __init__(self):
        lines = [
            line.replace("\n", "")
            for line in open("random.txt").readlines()
        ]
        print(lines)

    def run(self):
        while True:
            self.render()
            self.handle_input()

    def render(self):
        pass

    def handle_input(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == chr(17):
           sys.exit(0)


class Buffer:
    pass


class Cursor:
    pass


if __name__ == '__main__':
    editor = Editor()
    editor.run()
