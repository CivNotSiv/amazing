import random


def valid_cells(grid: list[list[int]],
                y: int, x: int) -> list[tuple[int, int]]:
    cells = []
    if x < len(grid[y]) - 1:
        if grid[y][x + 1] != 15 and grid[y][x] & 2:
            cells.append((y, x + 1))
    if x > 0:
        if grid[y][x - 1] != 15 and grid[y][x] & 8:
            cells.append((y, x - 1))

    if len(cells) == 0:
        if y < len(grid) - 1:
            if grid[y + 1][x] != 15 and grid[y][x] & 4:
                cells.append((y + 1, x))
        if y > 0:
            if grid[y - 1][x] != 15 and grid[y][x] & 1:
                cells.append((y - 1, x))
    return cells


def imperfect_play(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 15:
                continue
            walls = 0
            if grid[y][x] & 1:
                walls += 1
            if grid[y][x] & 2:
                walls += 1
            if grid[y][x] & 4:
                walls += 1
            if grid[y][x] & 8:
                walls += 1
            if walls == 3:
                cells = valid_cells(grid, y, x)
                if not cells:
                    continue
                rmy, rmx = random.choice(cells)
                if rmy < y:
                    grid[y][x] -= 1
                    grid[rmy][rmx] -= 4
                elif rmy > y:
                    grid[y][x] -= 4
                    grid[rmy][rmx] -= 1
                elif rmx < x:
                    grid[y][x] -= 8
                    grid[rmy][rmx] -= 2
                elif rmx > x:
                    grid[y][x] -= 2
                    grid[rmy][rmx] -= 8
                return grid, False
    return grid, True


def imperfect(grid: list[list[int]]) -> list[list[int]]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 15:
                continue
            walls = 0
            if grid[y][x] & 1:
                walls += 1
            if grid[y][x] & 2:
                walls += 1
            if grid[y][x] & 4:
                walls += 1
            if grid[y][x] & 8:
                walls += 1
            if walls == 3:
                cells = valid_cells(grid, y, x)
                if not cells:
                    continue
                rmy, rmx = random.choice(cells)
                if rmy < y:
                    grid[y][x] -= 1
                    grid[rmy][rmx] -= 4
                elif rmy > y:
                    grid[y][x] -= 4
                    grid[rmy][rmx] -= 1
                elif rmx < x:
                    grid[y][x] -= 8
                    grid[rmy][rmx] -= 2
                elif rmx > x:
                    grid[y][x] -= 2
                    grid[rmy][rmx] -= 8
    return grid
