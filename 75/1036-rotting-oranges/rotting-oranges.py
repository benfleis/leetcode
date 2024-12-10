#!/usr/bin/env python

# %% Cell 1
INVALID = -1
EMPTY = 0
FRESH = 1
ROTTEN = 2

def rot_oranges(grid: list[list[int]]) -> int:
    # grid support
    row_cnt = len(grid)
    col_cnt = len(grid[0]) if grid else 0
    def grid_state(pos):
        r, c = pos
        return grid[r][c] if 0 <= r < row_cnt and 0 <= c < col_cnt else INVALID

    def neighbors(row_col):
        (r, c) = row_col
        neighbors = [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]
        return filter(lambda x: grid_state(x) != INVALID, neighbors)

    # update spread in place; first calc all new rottens, then update
    spreaders = [
        (row, col) for col in range(col_cnt) for row in range(row_cnt)
        if grid[row][col] == ROTTEN
    ]

    round = 0
    while spreaders:
        next = set()
        for spreader in spreaders:
            for neighbor in neighbors(spreader):
                if grid_state(neighbor) == FRESH:
                    grid[neighbor[0]][neighbor[1]] = ROTTEN
                    next.add(neighbor)
        spreaders = next
        if spreaders:
            round += 1

    for row in grid:
        for state in row:
            if state == FRESH:
                return -1
    return round


def rot_oranges_holding(grid: list[list[int]]) -> int:
    # grid support
    row_cnt = len(grid)
    col_cnt = len(grid[0]) if grid else 0
    def is_in_grid(pos):
        r, c = pos
        return 0 <= r < row_cnt and 0 <= c < col_cnt

    def neighbors(rc):
        r, c = rc
        neighbors = [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]
        return filter(is_in_grid, neighbors)

    # all of these sets hold a tuple (row, col)
    rotten = set()
    fresh = set()
    ignore = set()  # holds both initial empties, and rottens after spread

    # init: every square lands in one of the above
    for row in range(row_cnt):
        for col in range(col_cnt):
            if grid[row][col] == EMPTY:
                ignore.add((row, col))
            elif grid[row][col] == FRESH:
                fresh.add((row, col))
            else: # == ROTTEN
                rotten.add((row, col))

    # iterate until rotten is empty, at which point return count IFF fresh == empty
    rounds = 0
    while fresh and rotten:
        print(f'ignore: {ignore}')
        print(f'fresh:  {fresh}')
        print(f'rotten: {rotten}')
        assert len(ignore) + len(fresh) + len(rotten) == row_cnt * col_cnt
        ignore |= rotten
        victims = set()
        for spreader in rotten:
            for (row, col) in (set(neighbors(spreader)) & fresh):
                cell = (row, col)
                victims.add(cell)
                fresh.remove(cell)
        rotten = victims
        rounds += 1

    return -1 if fresh else rounds

# %% Cell 2
tests = [
    ([[0,2]], 0),
    ([[1,2]], 1),
    ([[2,1,1],[1,1,0],[0,1,1]], 4),
    ([[2,1,1],[0,1,1],[1,0,1]], -1),
]

for grid,exp in tests:
    act = rot_oranges(grid)
    print(f'rot_oranges({grid}) -> {act}')
    assert act == exp, f"rot_oranges(...) -> {act} != {exp}"
else:
    print(f'All tests ({len(tests)}) passed.')
