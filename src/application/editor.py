import sys
import tty
import termios
from .commands.handle_editor_input_command import HandleEditorInputCommand
from .buffer import Buffer
from .cursor import Cursor
from .ansi import ANSI
from .history import History


class Editor:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, "r") as fp:
            lines = [line.replace("\n", "") for line in fp.readlines()]
        self.buffer = Buffer(lines)
        self.cursor = Cursor()
        self.history = History()

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
        char = sys.stdin.read(1)
        command = HandleEditorInputCommand(editor=self)
        command.execute(char)

    def save_file(self):
        with open(self.filepath, "w") as fp:
            fp.writelines([line + "\n" for line in self.buffer.lines])
