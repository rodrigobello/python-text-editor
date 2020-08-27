class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def move_to_col(self, col):
        return Cursor(self.row, col)

    def up(self, buffer):
        return Cursor(self.row - 1, self.col).clamp(buffer)

    def down(self, buffer):
        return Cursor(self.row + 1, self.col).clamp(buffer)

    def left(self, buffer):
        return Cursor(self.row, self.col - 1).clamp(buffer)

    def right(self, buffer):
        return Cursor(self.row, self.col + 1).clamp(buffer)

    def clamp(self, buffer):
        clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
        row = clamp(self.row, 0, buffer.line_count - 1)
        col = clamp(self.col, 0, buffer.line_length(row))
        return Cursor(row, col)
