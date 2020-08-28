class Buffer:
    def __init__(self, lines):
        self.lines = lines

    @property
    def line_count(self):
        return len(self.lines)

    def line_length(self, row):
        return len(self.lines[row])

    def insert(self, char, row, col):
        lines = self.lines.copy()
        lines[row] = lines[row][:col] + char + lines[row][col:]
        self.lines = lines

    def delete(self, row, col):
        lines = self.lines.copy()
        lines_arr = list(lines[row])
        del lines_arr[col]
        lines[row] = "".join(lines_arr)
        self.lines = lines

    def split_line(self, row, col):
        lines = self.lines.copy()
        lines[row:row + 1] = lines[row][:col], lines[row][col:]
        self.lines = lines

    def render(self):
        for line in self.lines:
            print(line, end="\r\n")
