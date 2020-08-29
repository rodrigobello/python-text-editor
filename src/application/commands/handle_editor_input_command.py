import sys
from src.application.constants import cursor as CURSOR_C, hotkeys as HOTKEYS_C


class HandleEditorInputCommand:
    def __init__(self, editor):
        self.editor = editor

    def execute(self, char):
        if char == HOTKEYS_C.EXIT_CHAR:  # ctrl+q
            sys.exit(0)
        elif char == HOTKEYS_C.UNDO_CHAR:  # ctrl+u
            try:
                self.editor.buffer, self.editor.cursor = self.editor.history.restore_snapshot()
            except self.editor.history.EmptyHistoryException:
                pass
        elif char == HOTKEYS_C.SAVE_CHAR:  # ctrl+w
            self.editor.save_file()
        elif char == HOTKEYS_C.CURSOR_UP_CHAR:  # ctrl+p
            self.editor.cursor.move(CURSOR_C.MOVE_UP, self.editor.buffer)
        elif char == HOTKEYS_C.CURSOR_DOWN_CHAR:  # ctrl+n
            self.editor.cursor.move(CURSOR_C.MOVE_DOWN, self.editor.buffer)
        elif char == HOTKEYS_C.CURSOR_LEFT_CHAR:  # ctrl+b
            self.editor.cursor.move(CURSOR_C.MOVE_LEFT, self.editor.buffer)
        elif char == HOTKEYS_C.CURSOR_RIGHT_CHAR:  # ctrl+f
            self.editor.cursor.move(CURSOR_C.MOVE_RIGHT, self.editor.buffer)
        elif char == HOTKEYS_C.SPLIT_LINE_CHAR:  # enter
            self.editor.history.save_snapshot(self.editor.buffer, self.editor.cursor)
            self.editor.buffer.split_line(
                self.editor.cursor.row,
                self.editor.cursor.col
            )
            self.editor.cursor.move(CURSOR_C.MOVE_DOWN, self.editor.buffer)
            self.editor.cursor.move(CURSOR_C.RESET_COLUMN, self.editor.buffer)
        elif char == HOTKEYS_C.DELETE_BEFORE_CURSOR_CHAR:  # backspace
            if self.editor.cursor.col > 0:
                self.editor.history.save_snapshot(
                    self.editor.buffer,
                    self.editor.cursor
                )
                self.editor.buffer.delete(
                    self.editor.cursor.row,
                    self.editor.cursor.col - 1
                )
                self.editor.cursor.move(CURSOR_C.MOVE_LEFT, self.editor.buffer)
        else:
            self.editor.history.save_snapshot(self.editor.buffer, self.editor.cursor)
            self.editor.buffer.insert(
                char, self.editor.cursor.row, self.editor.cursor.col
            )
            self.editor.cursor.move(CURSOR_C.MOVE_RIGHT, self.editor.buffer)
