from src.lib.utils import clamp
from src.application.constants import cursor as C


class Cursor:
    allowed_movements = C.MOVEMENTS

    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def move(self, movement, buffer):
        if movement not in self.allowed_movements:
            raise self.InvalidMovementException(f"Unknown movement {movement}")
        if movement == C.MOVE_UP:
            self._set_position(row=self.row - 1, col=self.col, buffer=buffer)
        elif movement == C.MOVE_DOWN:
            self._set_position(row=self.row + 1, col=self.col, buffer=buffer)
        elif movement == C.MOVE_LEFT:
            self._set_position(row=self.row, col=self.col - 1, buffer=buffer)
        elif movement == C.MOVE_RIGHT:
            self._set_position(row=self.row, col=self.col + 1, buffer=buffer)
        elif movement == C.RESET_COLUMN:
            self._set_position(row=self.row, col=0, buffer=buffer)

    def _set_position(self, row, col, buffer):
        self.row = clamp(row, 0, buffer.line_count - 1)
        self.col = clamp(col, 0, buffer.line_length(self.row))

    class InvalidMovementException(Exception):
        pass
