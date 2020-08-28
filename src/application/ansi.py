class ANSI:
    @classmethod
    def clear_screen(cls):
        print("[2J")

    @classmethod
    def move_cursor(cls, row, col):
        print(f"[{row + 1};{col + 1}H")
