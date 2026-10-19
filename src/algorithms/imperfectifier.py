import random as rand


def valid_cells(grid: list[list[int]], y: int,
                x: int) -> list[tuple[int, int]]:
    valid_cells = []
    if grid[y][x] & 2 and x < len(grid[y]) - 1 and grid[y][x + 1] != 15:
        valid_cells.append(tuple((y, x + 1)))
    if grid[y][x] & 8 and x > 0 and grid[y][x - 1] != 15:
        valid_cells.append(tuple((y, x - 1)))
    if grid[y][x] & 4 and y < len(grid) - 1 and grid[y + 1][x] != 15:
        valid_cells.append(tuple((y + 1, x)))
    if grid[y][x] & 1 and y > 0 and grid[y - 1][x] != 15:
        valid_cells.append(tuple((y - 1, x)))
    return valid_cells


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
                cells = valid_cells(grid, y, x)
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
