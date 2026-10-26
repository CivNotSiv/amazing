import random


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
        y = random.randrange(0, len(h_grid))
        x = random.randrange(0, len(h_grid[y]))
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

    rm_wall = random.choice(options)
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
