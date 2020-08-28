import sys
from src.application import constants as C


class HandleEditorInputCommand:
    def __init__(self, editor): # should receive a snapshot instead ?
        self.editor = editor

    def execute(self, char):
        # ASCII TABLE: http://www.physics.udel.edu/~watson/scen103/ascii.html
        if char == chr(17):  # ctrl+q
            sys.exit(0)
        elif char == chr(21):  # ctrl+u
            try:
                self.editor.buffer, self.editor.cursor = self.editor.history.restore_snapshot()
            except self.editor.history.EmptyHistoryException:
                pass
        elif char == chr(23):  # ctrl+w
            self.editor.save_file()
        elif char == chr(16):  # ctrl+p
            self.editor.cursor.move(C.CURSOR_MOVE_UP, self.editor.buffer)
        elif char == chr(14):  # ctrl+n
            self.editor.cursor.move(C.CURSOR_MOVE_DOWN, self.editor.buffer)
        elif char == chr(2):  # ctrl+b
            self.editor.cursor.move(C.CURSOR_MOVE_LEFT, self.editor.buffer)
        elif char == chr(6):  # ctrl+f
            self.editor.cursor.move(C.CURSOR_MOVE_RIGHT, self.editor.buffer)
        elif char == chr(13):  # enter
            self.editor.history.save_snapshot(self.editor.buffer, self.editor.cursor)
            self.editor.buffer.split_line(
                self.editor.cursor.row,
                self.editor.cursor.col
            )
            self.editor.cursor.move(C.CURSOR_MOVE_DOWN, self.editor.buffer)
            self.editor.cursor.move(C.CURSOR_RESET_COLUMN, self.editor.buffer)
        elif char == chr(127):  # backspace
            if self.editor.cursor.col > 0:
                self.editor.history.save_snapshot(
                    self.editor.buffer,
                    self.editor.cursor
                )
                self.editor.buffer.delete(
                    self.editor.cursor.row,
                    self.editor.cursor.col - 1
                )
                self.editor.cursor.move(C.CURSOR_MOVE_LEFT, self.editor.buffer)
        else:
            self.editor.history.save_snapshot(self.editor.buffer, self.editor.cursor)
            self.editor.buffer.insert(
                char, self.editor.cursor.row, self.editor.cursor.col
            )
            self.editor.cursor.move(C.CURSOR_MOVE_RIGHT, self.editor.buffer)
