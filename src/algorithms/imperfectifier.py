import random as rand


def available_dir(grid: list[list[int]],
                  current: tuple[int, int]) -> list[tuple[int, int]]:
    """
        Finds the available cells from around the current cell and
        adds them into a tuple
    """
    y, x = current
    walls = grid[y][x]
    valid: list[tuple[int, int]] = []
    if (walls & 1):
        if y - 1 >= 0 and grid[y - 1][x] != 15:
            valid.append((y - 1, x))
    if (walls & 2):
        if x + 1 < len(grid[y]) and grid[y][x + 1] != 15:
            valid.append((y, x + 1))
    if (walls & 4):
        if y + 1 < len(grid) and grid[y + 1][x] != 15:
            valid.append((y + 1, x))
    if (walls & 8):
        if x - 1 >= 0 and grid[y][x - 1] != 15:
            valid.append((y, x - 1))
    return valid
 

def imperfect(grid: list[list[int]]) -> list[list[int]]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            wall = 0
            if grid[y][x] == 15:
                continue
            if (grid[y][x] % 1):
                wall += 1
            if (grid[y][x] % 2):
                wall += 1
            if (grid[y][x] % 4):
                wall += 1
            if (grid[y][x] % 8):
                wall += 1
            if wall == 3:
                cells = available_dir(grid, (y, x))
                if not cells:
                    continue
                rm_wall = rand.choice(cells)
            if not rm_wall:
                continue
            rmy = rm_wall[0]
            rmx = rm_wall[1]
            if rmy - y > 0:
                grid[y][x] -= 1
                grid[rmy][rmx] -= 4
            if rmy - y < 0:
                grid[y][x] -= 4
                grid[rmy][rmx] -= 1
            if rmx - x > 0:
                grid[y][x] -= 8
                grid[rmy][rmx] -= 2
            if rmx - x < 0:
                grid[y][x] -= 2
                grid[rmy][rmx] -= 8
    return grid
