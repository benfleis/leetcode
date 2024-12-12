#!/usr/bin/env python

# %% Cell 1
def can_visit_all_rooms(room_keys: list[list[int]]) -> bool:
    visited = set()     # rooms we've visited and grabbed keys, adding to to_visit
    to_visit = set([0]) # rooms we've keys to

    while to_visit:
        print(f'visited={visited}')
        print(f'to_visit={to_visit}')
        room = to_visit.pop()
        visited.add(room)
        keys = set(room_keys[room])
        to_visit |= (keys - visited)
        print(f'to_visit += room_keys[{room}]={keys} = {to_visit}')
    print(f'visited={visited}')

    return len(visited) == len(room_keys)

# %% Cell 2
tests = [
    ([[]], True),
    ([[1], [2], [3], []], True),
    ([[1,3],[3,0,1],[2],[0]], False),
    ([[3], [2], [0], [1]], True),
    ([[3], [2], [2, 0], [3, 1]], True),
]

for room_keys,exp in tests:
    act = can_visit_all_rooms(room_keys)
    assert act == exp, f"visit_rooms(...) -> {act} != {exp}"
else:
    print(f'All tests ({len(tests)}) passed.')
