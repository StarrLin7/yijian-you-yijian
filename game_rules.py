from dataclasses import dataclass

BOARD_SIZE = 6
STARTING_CHANCES = 3
STEP = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1),
}

@dataclass(frozen=True)
class Arrow:
    row: int
    column: int
    symbol: str

@dataclass(frozen=True)
class MoveResult:
    status: str
    arrow: Arrow

STAGES = [
    [
        Arrow(0, 0, "→"),
        Arrow(0, 3, "↓"),
        Arrow(2, 5, "←"),
        Arrow(4, 1, "↑"),
        Arrow(5, 2, "→"),
    ],
    [
        Arrow(0, 1, "↓"),
        Arrow(1, 0, "→"),
        Arrow(1, 4, "↓"),
        Arrow(3, 1, "→"),
        Arrow(3, 3, "↓"),
        Arrow(5, 4, "←"),
    ],
    [
        Arrow(0, 0, "→"),
        Arrow(0, 2, "↓"),
        Arrow(2, 2, "←"),
        Arrow(2, 0, "↓"),
        Arrow(4, 0, "→"),
        Arrow(4, 4, "↑"),
        Arrow(1, 4, "←"),
        Arrow(1, 1, "↑"),
    ],
]

class Puzzle:
    def __init__(self, arrows, chances=STARTING_CHANCES):
        self.arrows = list(arrows)
        self.chances = chances

    def arrow_at(self, row, column):
        for arrow in self.arrows:
            if arrow.row == row and arrow.column == column:
                return arrow
        return None

    def is_clear_ahead(self, arrow):
        row_step, column_step = STEP[arrow.symbol]
        row = arrow.row + row_step
        column = arrow.column + column_step
        while 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE:
            if self.arrow_at(row, column) is not None:
                return False
            row += row_step
            column += column_step
        return True

    def choose(self, row, column):
        arrow = self.arrow_at(row, column)
        if arrow is None:
            return None
        if self.is_clear_ahead(arrow):
            self.arrows.remove(arrow)
            return MoveResult("leave", arrow)
        self.chances -= 1
        return MoveResult("blocked", arrow)

    @property
    def is_cleared(self):
        return not self.arrows

    @property
    def is_lost(self):
        return self.chances <= 0
