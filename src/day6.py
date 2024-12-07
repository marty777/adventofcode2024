
import src.util as util
from collections import defaultdict
from dataclasses import dataclass
from copy import deepcopy
from bisect import insort, bisect

DIRECTIONS = util.adjacency_4()

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
    next = util.coord_sum(guard.coord(), DIRECTIONS[guard.dir])
    if is_obstacle(grid, obstruction, next):
        guard.dir = (guard.dir + 1) % 4
    else:
        guard.x = next[0]
        guard.y = next[1]

# Advance the guard directly to next obstacle or off the map rather than 
# taking a single step
def guardstep_jump(obstacles_by_row, obstacles_by_column, guard, width, height):
    next = None
    obstacle_reached = False
    match guard.dir:
        case 0: # north
            # get the closest obstacle north of the guard position in this column
            next_obstacle_y = util.last_safe(obstacles_by_column[guard.x][:bisect(obstacles_by_column[guard.x], guard.y)])
            if next_obstacle_y == None:
                guard.y = -1 # leave the area
            else:
                guard.y = next_obstacle_y + 1
                obstacle_reached = True
        case 1: # east
            # get the closest obstacle east of the guard position in this row
            next_obstacle_x = util.first_safe(obstacles_by_row[guard.y][bisect(obstacles_by_row[guard.y], guard.x):])
            if next_obstacle_x == None:
                guard.x = width # leave the area
            else:
                guard.x = next_obstacle_x - 1
                obstacle_reached = True
        case 2: # south
            # get the closest obstacle south of the guard position in this column
            next_obstacle_y = util.first_safe(obstacles_by_column[guard.x][bisect(obstacles_by_column[guard.x], guard.y):])
            if next_obstacle_y == None:
                guard.y = height # leave the area
            else:
                guard.y = next_obstacle_y - 1
                obstacle_reached = True
        case 3: # west
            # get the closest obstacle west of the guard position in this row
            next_obstacle_x = util.last_safe(obstacles_by_row[guard.y][:bisect(obstacles_by_row[guard.y], guard.x)])
            if next_obstacle_x == None:
                guard.x = -1 # leave the area
            else:
                guard.x = next_obstacle_x + 1
                obstacle_reached = True
    if obstacle_reached: guard.dir = (guard.dir + 1) % 4

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
    # parse the grid into row/column obstacle indexes
    obstacles_by_row = [[] for y in range(height)]
    obstacles_by_column = [[] for x in range(width)]
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == '#':
                obstacles_by_column[x].append(y)
                obstacles_by_row[y].append(x)
    
    cycles_found = 0
    for obstruction in original_positions:
        if obstruction == guard.coord(): continue
        # copy the guard
        test_guard = deepcopy(guard)
        # copy the obstacle lookups and append the obstruction
        obstacles_by_row_with_obstruction = deepcopy(obstacles_by_row)
        obstacles_by_column_with_obstruction = deepcopy(obstacles_by_column)
        insort(obstacles_by_column_with_obstruction[obstruction[0]], (obstruction[1]))
        insort(obstacles_by_row_with_obstruction[obstruction[1]], (obstruction[0]))
        history = defaultdict(set)
        while True:
            guardstep_jump(obstacles_by_row_with_obstruction, obstacles_by_column_with_obstruction, test_guard, width, height)
            if test_guard.dir in history[test_guard.coord()]:
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
    guard = None
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == '^':
                guard = Guard(x,y,0)
                grid[(x,y)] = '.'
                break
        if guard is not None:
            break
    # find the set of distinct positions in the original guard route
    original_guard_positions = part1(grid, width, height, deepcopy(guard))
    # find the count of positions on the original guard route where adding an 
    # obstacle results in a cycle
    cycles_found = part2(grid, width, height, deepcopy(guard), original_guard_positions)
    print("Part 1:", len(original_guard_positions))
    print("Part 2:", cycles_found)
    