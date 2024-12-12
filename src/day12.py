
import src.util as util
from collections import defaultdict
from bisect import insort, bisect

DIRECTIONS = util.adjacency_4()
UP = DIRECTIONS[0]
RIGHT = DIRECTIONS[1]
DOWN = DIRECTIONS[2]
LEFT = DIRECTIONS[3]

# Find all points in a contiguous region to (x,y) which share the same symbol
# and add the new region to the regions list
def flood_region(x,y, grid, found, regions):
    gueue = []
    queue_next = [(x,y)]
    curr_group = set()
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        for pos in queue:
            if found[pos]:
                continue
            found[pos] = True
            curr_group.add(pos)

            for d in DIRECTIONS:
                next = util.coord_sum(pos,d)
                if grid[next] == grid[pos]:
                    if not found[next]:
                        queue_next.append(next)
    regions.append(curr_group)

# Run along the row/col for a directional border. 
# Return the count of elements as the perimeter part and the count of groups of 
# continguous elements as the sides part.
def directional_perimeter(border, dim):
    perimeter = 0
    sides = 0
    for d in range(dim):
        perimeter += len(border[d])
        left_count = 0
        if len(border[d]) == 0:
            continue
        
        last = None
        for i in range(len(border[d])):
            if last == None:
                sides += 1
            else:
                if border[d][i] != last + 1: #discontinuity
                    sides += 1
            last = border[d][i]
    return perimeter, sides

# General idea:
# Find all borders in the up, down, left and right directions by finding 
# elements in the region without a neighbor in that direction. Sort each 
# directional border by row/column.
# A straight edge is a contingious set of border cells in a direction on a 
# row/column. Any break in the set indicates a new edge.
def find_perimeter(region, width, height):
    ups = defaultdict(list)
    lefts =  defaultdict(list)
    rights =  defaultdict(list)
    downs =  defaultdict(list)
    sides = 0
    perimeter = 0
    # Build sorted lists of border cells in the up, down, left and right 
    # directions, indexed by row/column
    for p in region:
        if util.coord_sum(p, UP) not in region:
            insort(ups[p[1]], p[0])
        if util.coord_sum(p, DOWN) not in region:
            insort(downs[p[1]], p[0])
        if util.coord_sum(p, LEFT) not in region:
            insort(lefts[p[0]], p[1])
        if util.coord_sum(p, RIGHT) not in region:
            insort(rights[p[0]], p[1])
    # Find the perimeter and side counts in each row/column and border 
    # direction    
    up_perimeter, up_sides = directional_perimeter(ups, width)
    sides += up_sides
    perimeter += up_perimeter
    down_perimeter, down_sides = directional_perimeter(downs, width)
    sides += down_sides
    perimeter += down_perimeter
    left_perimeter, left_sides = directional_perimeter(lefts, height)
    sides += left_sides
    perimeter += left_perimeter
    right_perimeter, right_sides = directional_perimeter(rights, height)
    sides += right_sides
    perimeter += right_perimeter
    
    return perimeter, sides

def day12(lines):
    part1 = 0
    part2 = 0
    # Read the grid and dimensions as a defaultdict indexed by tuple (x,y)
    grid, width, height = util.read_grid_dict(lines)
    # Flood fill to find regions
    found = defaultdict(bool)
    regions = []
    for x in range(width):
        for y in range(height):
            if found[(x,y)]:
                continue
            flood_region(x,y,grid,found,regions)
    
    for r in regions:
        perimeter, sides = find_perimeter(r, width, height)
        part1 += len(r) * perimeter
        part2 += len(r) * sides

    print("Part 1:", part1)
    print("Part 2:", part2)
    