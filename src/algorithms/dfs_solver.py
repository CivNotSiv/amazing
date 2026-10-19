def _get_neighbor(grid: list[int], current: tuple[int, int]) -> list[
    tuple[int, int]]:
    '''
    returns a list holding tuples of coordinates of valid neighbors
    (this function does not track for parent/visited nodes).
    
    checks the current cell and compares it bitwise values of 1, 2, 4 and 8,
    these values represent the 'walls' of the cell in order of 'NESW'.
    This function also checks if the neighbors are valid (out of bounds/walls)
    
    lowkey stole ur func lel... now that I'm writing this I could've js used
    used ur func instead of remaking this...
    '''
    y, x = current
    cell = grid[y][x]
    neighbors: list[tuple[int, int]] = []
    if not cell & 1 and y > 0 and grid[y - 1][x] != 15:
        neighbors.append((y - 1, x))
    if not cell & 2  and x + 1 < len(grid[y]) and grid[y][x + 1] != 15:
        neighbors.append((y, x + 1))
    if not cell & 4 and y + 1 < len(grid) and grid[y + 1][x] != 15:
        neighbors.append((y + 1, x))
    if not cell & 8 and x - 1 >= 0 and grid[y][x - 1] != 15:
        neighbors.append((y, x - 1))
    return neighbors

def dfs(grid: list[int], start_exit: tuple[tuple[int, int]]) -> list[
    tuple[int, int]]:
    '''
    returns a list of a tuples that hold the coordinates of the path that was
    used to find the exit or an empty list if no path was found.

    uses a stack of valid coordinates from '_get_neighbor' to traverse
    through the maze in a LIFO (last in first out) way. This makes it so
    the algorithm travels to the deepest point until it finds a dead-end,
    making it backtrack to the last point where it can go into another
    direction going in order of 'NESW'.
    '''
    start, end = start_exit
    stack: list[tuple[int, int]] = [start]
    parents: dict[tuple[int, int], tuple[int, int]] = {start: None}
    while stack:
        current = stack.pop()
        if current == end:
            path: list[tuple[int, int]] = []
            node: tuple[int, int] = current
            while node is not None:
                path.append(node)
                node = parents[node]
            return path[::-1]
        for nxt in _get_neighbor(grid, current):
            if nxt not in parents:
                parents[nxt] = current
                stack.append(nxt)
    return []
