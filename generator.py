from typing import Any
import random as rand


ARGS: dict[str, Any] = {
        "WIDTH": 20,
        "HEIGHT": 20,
        # "ENTERY": "0,0,
        # "EXIT": 9, 4,
        # "OUTPUT_FILE": maze.txt,
        "PERFECT": True
    }


STAMP: list[list[int]] = [
    [1,0,1,0,1,1,1],
    [1,0,1,0,0,0,1],
    [1,1,1,0,1,1,1],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,1,1],
]

# STAMP: list[list[int]] = [
#     [0,0,0,0,0,0,0],
#     [0,0,1,0,0,1,0],
#     [0,0,0,0,0,0,0],
#     [0,1,0,0,0,0,1],
#     [0,0,1,1,1,1,0],
# ]


def init_grid(x: int, y: int) -> list[list[int]]:
    """
    generates a x by y grid then zeros it, then it itterates
    over the grid setting the default values
    """
    grid = [[col for col in range(x)]
            for row in range(y)]
    grid = [[(grid[i][j] * 0) + 15 for j in range(x)]
            for i in range(y)]
    return grid


def init_immutable(grid: list[list[int]]) -> list[tuple[int]]:
    """
    generates a list of tuples where the maze generator should
    not touch
    """
    origin: tuple[int, int] = round(len(grid[0]) / 2), round(len(grid) / 2)
    offset: tuple[int, int] = round(len(STAMP[0]) / 2), round(len(STAMP) / 2)
    immutable_grid = []
    s_line = 0
    if len(grid) < 9 or len(grid[0]) < 9:
        return immutable_grid
    for g_line in range(len(grid)):
        if g_line < origin[1] - offset[1] or g_line > origin[1] + offset[1]:
            continue
        for i in range(len(grid[0])):
            if i < origin[0] - offset[0] + 1 or s_line > len(STAMP) - 1:
                continue
            for s_pos in range(len(STAMP[s_line])):
                if STAMP[s_line][s_pos] == 1:
                    immutable_grid.append(tuple((g_line, i)))
                i += 1
            s_line += 1
            break
    return immutable_grid


class tree_set:
    def __init__(self, id_num: int) -> None:
        self.identiy = id_num
        self.parent: tree_set | None = None

    def update_parent(self, new_parent: "tree_set") -> None:
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

    def valid_connection(self, prospect: "tree_set") -> bool:
        if self.identiy == 0 or prospect.identiy == 0:
            return False
        return self._get_root() is not prospect._get_root()



def kruskal_algo(grid: list[list[int]], immutable: list[tuple[int]], seed: int) -> list[list[int]]:
    """
    explanation.
    1st,    we take the list of immutables and overlay them on the grid
            as we itterate over the grid assigning each cell its id the
            cells that are over an immutable position are assigned id 0
            so that during the verification setep we can skip over them

    2nd,    we set the random seed to be the given value, then we set 
            amount of connections based on grid size and if it can contain
            the desired stamp. then the generation begins
    
    3rd,    for the amount of req connections we loop over the maze,
            we check the elements surrounding the randomly selected cell
            and if the element is a valid target wwe add it to the options
            list, then we randomly selsect from the options, if there
            are no options we start again.
    
    4rd,    we update the hidden grid to reflect the desired change
            this is done by updating the parent, if the target cell isnt
            the parent of its tree we navigate to the top of the target
            tree and make it point to the current cell, thus inheriting
            the tree into its own tree

    5st,    then we update the grid to show the changes in the hidden grid
            we update the target and the origin cells at the same time with
            the fucked up if else block, it should be fine because only x or y
            will be pos or neg at a time so it shouldnt cause trubel 
    
    6rd,    anyway that continues until the desird connections are reached
            then it just returns the grid
    """
    hidden_set_grid: list[list[int]] = [row[:] for row in grid]
    grid_size: tuple = tuple((len(grid), len(grid[0])))
    identiy = 1
    for line in range(len(hidden_set_grid)):
        for cell in range(len(hidden_set_grid[line])):
            if any(t == tuple((line,cell)) for t in immutable):
                hidden_set_grid[line][cell] = tree_set(0)
                continue
            hidden_set_grid[line][cell] = tree_set(identiy)
            identiy += 1

    rand.seed(seed)
    connections = (grid_size[0] * grid_size[1]) - 1
    if grid_size[0] > 9 and grid_size[1] > 9:
        connections -= len(immutable)
    while connections:
        y = rand.randrange(0, len(hidden_set_grid))
        x = rand.randrange(0, len(hidden_set_grid[y]))
        cell_origin = tuple((y, x))

        options = []
        if x - 1 >= 0 and hidden_set_grid[y][x].valid_connection(hidden_set_grid[y][x - 1]):
            options.append(tuple((y, x - 1)))
        if x + 1 < grid_size[1] and hidden_set_grid[y][x].valid_connection(hidden_set_grid[y][x + 1]):
            options.append(tuple((y, x + 1)))
        if y - 1 >= 0 and hidden_set_grid[y][x].valid_connection(hidden_set_grid[y - 1][x]):
            options.append(tuple((y - 1, x)))
        if y + 1 < grid_size[0] and hidden_set_grid[y][x].valid_connection(hidden_set_grid[y + 1][x]):
            options.append(tuple((y + 1, x)))
        if len(options) == 0:
            continue

        connections -= 1
        cell_candidate = rand.choice(options)
        hidden_set_grid[cell_candidate[0]][cell_candidate[1]].update_parent(hidden_set_grid[cell_origin[0]][cell_origin[1]])
        if (cell_origin[0] - cell_candidate[0]) < 0:
            grid[cell_origin[0]][cell_origin[1]] -= 4
            grid[cell_candidate[0]][cell_candidate[1]] -= 1
        elif (cell_origin[0] - cell_candidate[0]) > 0:
            grid[cell_origin[0]][cell_origin[1]] -= 1
            grid[cell_candidate[0]][cell_candidate[1]] -= 4

        if (cell_origin[1] - cell_candidate[1]) < 0:
            grid[cell_origin[0]][cell_origin[1]] -= 2
            grid[cell_candidate[0]][cell_candidate[1]] -= 8
        elif (cell_origin[1] - cell_candidate[1]) > 0:
            grid[cell_origin[0]][cell_origin[1]] -= 8
            grid[cell_candidate[0]][cell_candidate[1]] -= 2
    return grid


def print_maze(grid: list[list[int]]) -> None:
    """
    this is miserable. 
    """
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print("+", end="")
            if grid[y][x] & 1:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        for x in range(len(grid[y])):
            if grid[y][x] & 8:
                print("|", end="")
            else:
                print(" ", end="")
            print("   ", end="")
        if grid[y][-1] & 2:
            print("|")
        else:
            print(" ")

    print("+", end="")
    for cell in grid[-1]:
        if cell & 4:
            print("---+", end="")
        else:
            print("   +", end="")

    print()


def generator(args: dict[str, Any]) -> list[list[int]]:
    """
    Refactor this to takein whatever format the parser outputed
    using pydantic base model to validate would be sick, then 
    pass the x, y, perfect and the EE tuples
    """
    y: int = args.get("HEIGHT")
    x: int = args.get("WIDTH")

    grid: list[list[int]] = init_grid(x, y)
    grid = kruskal_algo(grid, init_immutable(grid), 42)
    print_maze(grid)

    return grid


if __name__ == "__main__":
    generator(ARGS)
