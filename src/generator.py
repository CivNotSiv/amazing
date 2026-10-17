import random as rand
from .algorithms import kruskal_algo, tree_set, bfs
from enum import Enum


STAMP: list[list[int]] = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class generate():

    class Style(Enum):
        DEFAULT = ("■", "■", "■", "■", "x")
        THINISH = ("■", "║", "═", "╋", "-")
        SPIKEYS = ("┼", "│", "─", "┼", "■")
        BALLSEY = ("𝚘", "│", "─", "𝚘", "♦")
        BREAILY = (" ", "⢸", "⠒", "⣿", "■")
        THISWAY = ("↺", "⇵", "⇌", "↺", "☹")
        AMOUNGS = ("ඞ", "ඞ", "ඞ", "ඞ", "⚠")

    DIRECTIONS: dict[tuple[int, int], str] = {
        (-1, 0): "N",
        (1, 0): "S",
        (0, 1): "E",
        (0, -1): "W",
    }

    def __init__(self, size: tuple[int, int], seed: int,
                 perfect: bool, selected: Style | None,
                 solved: list[tuple[int, int]]):
        rand.seed(seed)
        self.size = size
        self.perfect = perfect

        self.grid: list[list[int]] = []
        self.hidden_grid: list[list[tree_set]] = []
        self.ignore: list[tuple[int, int]] = []

        self.__init_grid__()
        self.__init_immutable__(STAMP)
        self.__init_hidden__()
        self.solved: list[tuple[int, int]] = solved

        self.connections = size[0] * size[1] - 1
        if size[0] >= 9 and size[1] >= 9:
            self.connections -= len(self.ignore)

        if selected is None:
            self.selected = self.Style.DEFAULT
        else:
            self.selected = selected

    def __init_grid__(self) -> None:
        """
        generates a x by y grid then zeros it, then it itterates
        over the grid setting the default values
        """
        self.grid = [[col for col in range(self.size[0])]
                     for row in range(self.size[1])]
        self.grid = [[(self.grid[i][j] * 0) + 15 for j in range(self.size[0])]
                     for i in range(self.size[1])]

    def __init_immutable__(self, stamp: list[list[int]]) -> None:
        """
        generates a list of tuples where the maze generator should
        not touch
        """
        if len(self.grid) < 9 or len(self.grid[0]) < 9:
            return

        stamp_y = (len(self.grid) - len(stamp)) // 2
        stamp_x = (len(self.grid[0]) - len(stamp[0])) // 2
        for i in range(len(stamp)):
            for j in range(len(stamp[i])):
                if stamp[i][j] == 1:
                    self.ignore.append((stamp_y + i, stamp_x + j))

    def __init_hidden__(self) -> None:
        """
        inits the hidden grid, we take the list of immutables and overlay
        them on the grid as we itterate over the grid assigning each cell
        its id the cells that are over an ignore position are assigned
        id 0 so that during the verification setep we can skip over them
        """
        self.hidden_grid = [[tree_set(0) for _ in row] for row in self.grid]
        identiy = 1
        for line in range(len(self.hidden_grid)):
            for cell in range(len(self.hidden_grid[line])):
                if any(t == tuple((line, cell)) for t in self.ignore):
                    continue
                self.hidden_grid[line][cell] = tree_set(identiy)
                identiy += 1

    def kruskal(self) -> list[list[int]]:
        for _ in range(self.connections):
            self.grid = kruskal_algo(self.grid, self.hidden_grid)
            self.connections -= 1
        return self.grid

    def kruskal_play(self) -> list[list[int]]:
        if self.connections:
            self.grid = kruskal_algo(self.grid, self.hidden_grid)
            self.connections -= 1
        return (self.grid)

    def solve(self, start_exit: list[tuple[int, int]]) -> None:
        self.solved = bfs(self.grid, start_exit)

    def next_style(self) -> None:
        members = list(self.Style)
        current = members.index(self.selected)
        self.selected = members[(current + 1) % len(members)]

    def draw_maze(self) -> str:
        """
        this is miserable.
        """
        cornor = self.selected.value[0]
        wall_v = self.selected.value[1]
        wall_h = self.selected.value[2]
        fortys = self.selected.value[3]
        path = self.selected.value[4]
        line = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                line.append(f"{cornor}")
                if self.grid[y][x] & 1:
                    line.append(f"{wall_h}{wall_h}{wall_h}")
                else:
                    line.append("   ")
            line.append(f"{cornor}\n")

            for x in range(len(self.grid[y])):
                if self.grid[y][x] & 8:
                    line.append(f"{wall_v}")
                else:
                    line.append(" ")
                if self.grid[y][x] == 15:
                    line.append(f"{fortys}{fortys}{fortys}")
                elif any(t == tuple((y, x)) for t in self.solved):
                    line.append(f" {path} ")
                else:
                    line.append("   ")
            if self.grid[y][-1] & 2:
                line.append(f"{wall_v}\n")
            else:
                line.append(" \n")

        line.append(f"{cornor}")
        for cell in self.grid[-1]:
            if cell & 4:
                line.append(f"{wall_h}{wall_h}{wall_h}{cornor}")
            else:
                line.append(f"   {cornor}")
        line.append("\n")
        return "".join(line)

    def _path_to_exit(self) -> str:
        steps: list[str] = ["\n"]
        for (y1, x1), (y2, x2) in zip(self.solved, self.solved[1:]):
            delta = (y2 - y1, x2 - x1)
            try:
                steps.append(self.DIRECTIONS[delta])
            except KeyError:
                return ""
        return str("".join(steps))

    def export_maze(self, filename: str,
                    start_exit: list[tuple[int, int]]) -> None:
        out_str = "\n".join(
            "".join(f"{cell:x}" for cell in row) for row in self.grid
        )
        start = str(start_exit[0]).strip("()")
        exit_ = str(start_exit[1]).strip("()")
        start = start + "          #start (y,x)\n"
        exit_ = exit_ + "          #exit (y,x)"
        with open(filename, "w") as fd:
            fd.write(out_str)
            fd.write("\n\n")
            fd.write(start)
            fd.write(exit_)
            fd.write(self._path_to_exit())
