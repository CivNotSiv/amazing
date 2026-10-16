
def available_dir(grid: list[list[int]],
                  current: tuple[int, int]) -> list[tuple[int, int]]:
    """
        Finds the available cells from around the current cell and
        adds them into a tuple
    """
    y, x = current
    walls = grid[y][x]
    valid: list[tuple[int, int]] = []
    if not (walls & 1):
        if y - 1 >= 0 and grid[y - 1][x] != 15:
            valid.append((y - 1, x))
    if not (walls & 2):
        if x + 1 < len(grid[y]) and grid[y][x + 1] != 15:
            valid.append((y, x + 1))
    if not (walls & 4):
        if y + 1 < len(grid) and grid[y + 1][x] != 15:
            valid.append((y + 1, x))
    if not (walls & 8):
        if x - 1 >= 0 and grid[y][x - 1] != 15:
            valid.append((y, x - 1))
    return valid


def bfs(grid: list[list[int]],
        start_exit: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
        returns a tuple of all valid cells it went through while
        navigating
        loops over queue until either the exit is reached or queue
        is depleated
    """
    start = start_exit[0]
    queue: list[tuple[tuple[int, int], list[tuple[int, int]]]] = [
        (start, [start])]
    visited: set[tuple[int, int]] = {start}

    while queue:
        current, path = queue.pop(0)
        if current == start_exit[1]:
            return path
        for next_pos in available_dir(grid, current):
            if next_pos not in visited:
                visited.add(next_pos)
                new_path = path + [next_pos]
                queue.append((next_pos, new_path))
    return start_exit
