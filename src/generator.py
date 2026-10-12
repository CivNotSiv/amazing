import random as rand
from enum import Enum



STAMP: list[list[int]] = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class tree_set():
    def __init__(self, id_num: int) -> None:
        self.identiy = id_num
        self.parent: tree_set | None = None

    def new_root(self, new_parent: "tree_set") -> None:
        self_root = self._get_root()
        new_root = new_parent._get_root()
        if self_root is new_root:
            return
        self_root.parent = new_root

    def _get_root(self) -> "tree_set":
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    def validate(self, prospect: "tree_set") -> bool:
        if self.identiy == 0 or prospect.identiy == 0:
            return False
        return self._get_root() is not prospect._get_root()


def kruskal_algo(grid: list[list[int]],
                 h_grid: list[list[tree_set]]) -> list[list[int]]:
    """
    explanation.
    1rd,    we check the elements surrounding the randomly selected cell
            and if the element is a valid target wwe add it to the options
            list, then we randomly selsect from the options, if there
            are no options we start again.

    2rd,    we update the hidden grid to reflect the desired change
            this is done by updating the parent, if the target cell isnt
            the parent of its tree we navigate to the top of the target
            tree and make it point to the current cell, thus inheriting
            the tree into its own tree

    3st,    then we update the grid to show the changes in the hidden grid
            we update the target and the origin cells at the same time with
            the fucked up if else block, it should be fine because only x or y
            will be pos or neg at a time so it shouldnt cause trubel

    4rd,    anyway that continues until the desird connections are reached
            then it just returns the grid
    """
    while True:
        y = rand.randrange(0, len(h_grid))
        x = rand.randrange(0, len(h_grid[y]))
        cell = tuple((y, x))

        options = []
        if x - 1 >= 0 and h_grid[y][x].validate(h_grid[y][x - 1]):
            options.append(tuple((y, x - 1)))
        if x + 1 < len(grid[0]) and h_grid[y][x].validate(h_grid[y][x + 1]):
            options.append(tuple((y, x + 1)))
        if y - 1 >= 0 and h_grid[y][x].validate(h_grid[y - 1][x]):
            options.append(tuple((y - 1, x)))
        if y + 1 < len(grid) and h_grid[y][x].validate(h_grid[y + 1][x]):
            options.append(tuple((y + 1, x)))
        if len(options) == 0:
            continue
        break

    rm_wall = rand.choice(options)
    h_grid[rm_wall[0]][rm_wall[1]].new_root(h_grid[cell[0]][cell[1]])
    if (cell[0] - rm_wall[0]) < 0:
        grid[cell[0]][cell[1]] -= 4
        grid[rm_wall[0]][rm_wall[1]] -= 1
    elif (cell[0] - rm_wall[0]) > 0:
        grid[cell[0]][cell[1]] -= 1
        grid[rm_wall[0]][rm_wall[1]] -= 4

    if (cell[1] - rm_wall[1]) < 0:
        grid[cell[0]][cell[1]] -= 2
        grid[rm_wall[0]][rm_wall[1]] -= 8
    elif (cell[1] - rm_wall[1]) > 0:
        grid[cell[0]][cell[1]] -= 8
        grid[rm_wall[0]][rm_wall[1]] -= 2
    return grid


class generate():
    def __init__(self, size: tuple[int, int], seed: int, perfect: bool, selected: list[str] | None):
        rand.seed(seed)
        self.size = size
        self.perfect = perfect

        self.grid: list[list[int]] = []
        self.hidden_grid: list[list[tree_set]] = []
        self.ignore: list[tuple[int, int]] = []

        self.__init_grid__()
        self.__init_immutable__(STAMP)
        self.__init_hidden__()

        self.connections = size[0] * size[1] - 1
        if size[0] >= 9 and size[1] >= 9:
            self.connections -= len(self.ignore)

        if selected == None:
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

    class Style(Enum):
        DEFAULT = ("■", "■", "■", "■")
        THINISH = ("■", "║", "═", "╋")
        ROADIES = ("╬", "║", "═", "╬")
        SPIKEYS = ("┼", "│", "─", "┼")
        BALLSEY = ("𝚘", "│", "─", "𝚘")
        BREAILY = (" ", "⢸", "⠒", "⣿")
        THISWAY = ("↺", "⇵", "⇌", "↺")
        AMOUNGS = ("ඞ", "ඞ", "ඞ", "ඞ")

    def next_style(self) -> "style":
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

    def export_maze(self) -> None:
        return
