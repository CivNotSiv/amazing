import random

_DIRS: tuple[tuple[int, int, int, int], ...] = (
    (1, -1, 0, 4),
    (2, 0, 1, 8),
    (4, 1, 0, 1),
    (8, 0 ,-1 ,2)
)

def dfs_generate(grid: list[list[int]],
                 start: tuple[int, int],
                 stamp: list[tuple[int, int]]) -> list[list[int]]:
    '''
    Starts from cell 'start' and checks the surrounding cells for valid moves
    within the options provided by '_DIRS'. Then breaks the walls and creates 
    a path to the valid cells and adds current cell to seen. 
    
    If no valid options found pop current item in stack and backtrack and
    continue traversing from the last point that has options available.
    '''
    height, width = len(grid), len(grid[0])
    seen: set[tuple[int, int]] = set(stamp) | {start}
    stack: list[tuple[int, int]] = [start]
    while stack:
        y, x = stack[-1]
        options: list[list[int, int, int, int]] = []
        for bit, delta_y, delta_x, opposite in _DIRS:
            new_y = y + delta_y
            new_x = x + delta_x
            if (0 <= new_y < height and 0 <= new_x < width
                and (new_y, new_x) not in seen):
                options.append((bit, new_y, new_x, opposite))
        if not options:
            stack.pop()
            continue
        bit, new_y, new_x, opposite = random.choice(options)
        grid[y][x] &= ~bit
        grid[new_y][new_x] &= ~opposite
        seen.add((new_y, new_x))
        stack.append((new_y, new_x))
    return grid
