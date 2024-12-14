
import src.util as util
from dataclasses import dataclass

PRINT_TREE = True # Set to True to enable printing the part 2 tree step

@dataclass
class Robot:
    startpos:tuple
    pos:tuple
    vel:tuple
    def reset(self):
        self.pos = self.startpos
    def step(self, width, height):
        next_pos_x = (self.pos[0] + self.vel[0]) % width
        next_pos_y = (self.pos[1] + self.vel[1]) % height
        self.pos = (next_pos_x, next_pos_y)

# Scan the pattern formed by the robots and return true if horizontal lines
# appear that exceed the cutoff parameters for count and length
def tree_scan(robots, width, height, min_horizontal_line_len, min_horizontal_lines):
    grid = []
    for y in range(height):
        grid.append([])
        for x in range(width):
            grid[y].append(0)
    for r in robots:
        grid[r.pos[1]][r.pos[0]] += 1
    # look for horizontal lines
    row_longest_line = [0] * height
    for y in range(height):
        curr_line = 0
        max_line = -1
        for x in range(width):
            if grid[y][x] == 0:
                if max_line == -1 or curr_line > max_line:
                    max_line = curr_line
                curr_line = 0
            else:
                curr_line += 1
        row_longest_line[y] = max_line
    horizontal_line_rows = 0
    for y in range(height):
        if row_longest_line[y] >= min_horizontal_line_len:
            horizontal_line_rows += 1
    return horizontal_line_rows >= min_horizontal_lines

def print_grid(robots, width, height):
    for y in range(height):
        for x in range(width):
            r_count = 0
            for r in robots:
                if r.pos == (x,y):
                    r_count += 1
            if r_count > 0:
                print("#", end='')
            else:
                print(".", end='')
        print("")

def day14(lines):
    part1 = 0
    part2 = 0
    width = 101
    height =103
    robots = []
    for i in range(len(lines)):
        vals = util.numbers_in_string(lines[i])
        robot = Robot((vals[0],vals[1]),(vals[0],vals[1]),(vals[2],vals[3]))
        robots.append(robot)

    # Part 1: Run robots forward 100 steps and count robots in quadrants
    for i in range(100):
        for j in range(len(robots)):
            robots[j].step(width, height)
    quadrant1 = 0
    quadrant2 = 0
    quadrant3 = 0
    quadrant4 = 0
    for j in range(len(robots)):
        r = robots[j]
        if r.pos[0] < width//2 and r.pos[1] < height//2:
            quadrant1 += 1
        elif r.pos[0] > width//2 and r.pos[1] < height//2:
            quadrant2 += 1
        elif r.pos[0] < width//2 and r.pos[1] > height//2:
            quadrant3 += 1
        elif r.pos[0] > width//2 and r.pos[1] > height//2:
            quadrant4 += 1
    part1 = quadrant1 * quadrant2 * quadrant3 * quadrant4

    # Reset robots to original position
    for r in robots:
        r.reset()
    
    # Part 2: Run robots forward until a tree (or at least a suitable number 
    # of horizontal lines) is present
    min_horizontal_line_length = 5
    min_horizontal_line_count = 5
    step = 0
    while True:
        for r in robots:
            r.step(width, height)
        step += 1
        if(tree_scan(robots, width, height, min_horizontal_line_length, min_horizontal_line_count)):
            part2 = step
            if PRINT_TREE:
                print_grid(robots, width, height)
            break
    print("Part 1:", part1)
    print("Part 2:", part2)
    