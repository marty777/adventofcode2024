
import src.util as util
from collections import defaultdict
from dataclasses import dataclass
from copy import deepcopy

@dataclass 
class Guard:
    x: int
    y: int
    dir: int
    def coord(self):
        return (self.x, self.y)

# Test if the guard has left the area
def outside(guard, width, height):
    return (guard.x < 0 or guard.x >= width or guard.y < 0 or guard.y >= height)

# Test if the given position contains an obstacle, optionally passing the 
# position of an extra obstruction
def is_obstacle(grid, obstruction, pos): 
    if obstruction is not None and pos == obstruction: return True
    return grid[pos] == '#'

# Advance the guard one step
def guardstep(grid, guard, obstruction):
    next = None
    match guard.dir:
        case 0: # north
            next = (guard.x, guard.y-1)
        case 1: # east
            next = (guard.x+1, guard.y)
        case 2: # south
            next = (guard.x, guard.y+1)
        case 3: # west 
            next = (guard.x-1, guard.y)
    if is_obstacle(grid, obstruction, next):
        guard.dir = (guard.dir + 1) % 4
    else:
        guard.x = next[0]
        guard.y = next[1]

# Advance the guard until they leave the area. Return the set of distinct 
# coords visited
def part1(grid, width, height, guard):
    touched = set()
    touched.add((guard.x,guard.y)) # include starting point
    while True:
        guardstep(grid, guard, None)
        if outside(guard, width, height):
            break
        touched.add(guard.coord())
    return touched

# For each coordinate the original guard reached add an obstruction and 
# test if the guard enters a cycle. Return the total number of obstruction
# positions that result in a cycle.
def part2(grid, width, height, guard, original_positions):
    cycles_found = 0
    for obstruction in original_positions:
        history = defaultdict(set)
        test_guard = deepcopy(guard)
        while True:
            guardstep(grid, test_guard, obstruction)
            if test_guard.coord() in history and test_guard.dir in history[test_guard.coord()]:
                cycles_found += 1
                break
            if outside(test_guard, width, height):
                break
            history[test_guard.coord()].add(test_guard.dir)
    return cycles_found

def day6(lines):
    # read the grid and dimensions as a defaultdict indexed by tuple (x,y)
    grid, width, height = util.read_grid_dict(lines)
    # find the guard
    guard = (0,0)
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == '^':
                guard = Guard(x,y,0)
                grid[(x,y)] = '.'
    # find the set of distinct positions in the original guard route
    original_guard_positions = part1(grid, width, height, deepcopy(guard))
    # find the count of positions on the original guard route where adding an 
    # obstacle results in a cycle
    cycles_found = part2(grid, width, height, deepcopy(guard), original_guard_positions)
    print("Part 1:", len(original_guard_positions))
    print("Part 2:", cycles_found)
    