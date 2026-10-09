from typing import Any


ARGS: dict[str, Any] = {
        "WIDTH": 13,
        "HEIGHT": 14,
        # "ENTERY": "0,0,
        # "EXIT": 9, 4,
        # "OUTPUT_FILE": maze.txt,
        "PERFECT": True
    }


STAMP: list[list[int]] = [
    [15,0,0,0,15,15,15],
    [15,0,0,0,0,0,15],
    [15,15,15,0,15,15,15],
    [0,0,15,0,15,0,0],
    [0,0,15,0,15,15,15],
]


def stamp_42(grid: list[list[int]]) -> list[list[int]]:
    """
    This function iterates over the grid waiting for the pos
    where pos < origin - 2, aka the first line where the stamp
    needs to be present, then it moves across the line until 
    the pos where the stamp needs to begin (origin - 4) and
    itterates over the stamp until its finished
    """
    origin: tuple[int, int] = (len(grid[0]) / 2), round(len(grid) / 2)
    s_line = -1
    for g_line in range(len(grid)):
        if g_line < origin[1] - 2 or g_line > origin[1] + 2:
            continue
        for i in range(len(grid[0])):
            if i < origin[0] - 4:
                continue
            s_line += 1
            for s_pos in range(len(STAMP[0])):
                grid[g_line][i] = STAMP[s_line][s_pos]
                i += 1
            break
    return grid


def init_grid(x: int, y: int) -> list[list[int]]:
    """
    generates a x by y grid then zeros it, then it itterates
    over the grid setting the default values, should the grid
    be big enough it stamps the 42 onto it
    """
    grid = [[col for col in range(x)]
            for row in range(y)]
    grid = [[grid[i][j] * 0 for j in range(x)]
            for i in range(y)]

    line = 0
    for row in grid:
        grid[line][0] = row[0] + 2
        grid[line][x - 1] = row[x - 1] + 8
        if line == 0:
            grid[line] = list(map(lambda x: x + 1, row))
        if line == y - 1:
            grid[line] = list(map(lambda x: x + 4, row))
        line += 1
    if x >= 10 and y >= 9:
        grid = stamp_42(grid)
    return grid


def generator(args: dict[str, Any]) -> list[list[int]]:
    """
    Refactor this to takein whatever format the parser outputed
    using pydantic base model to validate would be sick, then 
    pass the x, y, perfect and the EE tuples
    """
    y: int = args.get("HEIGHT")
    x: int = args.get("WIDTH")

    grid: list[list[int]] = init_grid(x, y)
    for row in grid:
        print(f"{row}")
    return grid


if __name__ == "__main__":
    generator(ARGS)
