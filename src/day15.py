
import src.util as util
from dataclasses import dataclass

DIRECTIONS = util.arrow_dirs()

@dataclass
class Box:
    id:int
    pos:tuple
    def score(self):
        return self.pos[0] + 100*self.pos[1]

@dataclass
class Robot:
    pos:tuple
    move_index:int
    moves:list
    def step(self, grid, boxes, wide=False):
        box_offset = (1,0)
        # build a lookup of current box positions
        box_positions = {}
        for b in boxes:
            box_positions[b.pos] = b.id
            if wide:
                box_positions[util.coord_sum(b.pos, box_offset)] = b.id
        # Determine next position of robot, if able to move
        move_dir = self.moves[self.move_index]
        robot_next = util.coord_sum(self.pos, DIRECTIONS[move_dir])
        # Increment move count
        self.move_index = (self.move_index + 1) % len(self.moves)
        # Determine any box or boxes affected by move
        next_positions = {robot_next}
        new_positions = {robot_next}
        box_ids = set()
        # Repeatedly add boxes to move group until no more found
        while True:
            new_boxes = set()
            for p in new_positions:
                if p in box_positions and box_positions[p] not in box_ids:
                    new_boxes.add(box_positions[p])
                    box_ids.add(box_positions[p])
            new_positions.clear()
            for box_id in new_boxes:
                next_box_positions = {util.coord_sum(boxes[box_id].pos, DIRECTIONS[move_dir])}
                if wide:
                    next_box_positions.add(util.coord_sum(util.coord_sum(boxes[box_id].pos, box_offset), DIRECTIONS[move_dir]))
                new_positions = new_positions | next_box_positions
                next_positions = next_positions | next_box_positions
            if len(new_boxes) == 0:
                break
        # Determine if the group can move
        can_move = True
        for p in next_positions:
            if grid[p] == '#':
                can_move = False
                break
        if not can_move:
            return
        # Move the box group and the robot
        for box_id in box_ids:
            boxes[box_id].pos = util.coord_sum(boxes[box_id].pos, DIRECTIONS[move_dir])
        self.pos = robot_next

# Read the regular grid, robot and boxes
def read_grid(grid_lines, moves):
    grid, width, height = util.read_grid_dict(grid_lines)
    boxes = []
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == '@':
                robot = Robot((x,y), 0, moves)
                grid[(x,y)] = '.'
            elif grid[(x,y)] == 'O':
                boxes.append(Box(len(boxes), (x,y)))
                grid[(x,y)] = '.'
    return grid, width, height, robot, boxes

# Read the expanded grid, robot and boxes
def read_widegrid(grid_lines, moves):
    lines2 = []
    for line in grid_lines:
        line2 = ''
        for c in list(line):
            if c == '#':
                line2 += '##'
            elif c == 'O':
                line2 += '[]'
            elif c == '@':
                line2 += '@.'
            else:
                line2 += '..'
        lines2.append(line2)
    grid, width, height = util.read_grid_dict(lines2)
    boxes = []
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == '@':
                robot = Robot((x,y), 0, moves)
                grid[(x,y)] = '.'
            elif grid[(x,y)] == '[' and grid[(x+1,y)] == ']':
                boxes.append(Box(len(boxes), (x,y)))
                grid[(x,y)] = '.'
                grid[(x+1,y)] = '.'
    return grid, width, height, robot, boxes

def day15(lines):
    part1 = 0
    part2 = 0

    # Read input sections separated by blank lines
    sections = util.sections(lines)

    # Process the move section
    moves = []
    for line in sections[1]:
        for m in list(line):
            moves.append(m)
    
    # Read the grid section and set up the robot and boxes
    grid, width, height, robot, boxes = read_grid(sections[0], moves)
    # Step robot through part 1
    for i in range(len(robot.moves)):
        robot.step(grid, boxes, wide=False)
    # Score part 1
    for b in boxes:
        part1 += b.score()

    # Read the widened grid and set up the robot and boxes
    grid2, width2, height2, robot2, boxes2 = read_widegrid(sections[0], moves)
    # Step robot through part2
    for i in range(len(robot2.moves)):
        robot2.step(grid2, boxes2, wide=True)
    # Score part 2
    for b in boxes2:
        part2 += b.score()

    print("Part 1:", part1)
    print("Part 2:", part2)
    