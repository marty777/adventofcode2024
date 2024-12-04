
import src.util as util

def sample_grid(grid,x,y,pattern, matches):
    match0 = True
    match1 = True
    for i in range(len(pattern)):
        c = grid[util.coord_sum(pattern[i],(x,y))]
        if c != matches[0][i]: match0 = False
        if c != matches[1][i]: match1 = False
        if not (match0 or match1): break
    return 1 if match0 ^ match1 else 0 # xor 

def day4(lines):
    part1 = 0
    part2 = 0
    # read the grid as a defaultdict (defaulting to '.'), plus the dimensions
    grid, width, height = util.read_grid_dict(lines)
    part1_matches = ['XMAS', 'SAMX']    
    part2_matches = ['MAS', 'SAM']    
    horizontal = [(x,0) for x in range(4)]
    vertical = [(0,x) for x in range(4)]
    diagonal1 = [(x,x) for x in range(4)]
    diagonal2 = [(3-x,x) for x in range(4)]
    cross1 = [(x,x) for x in range(3)]
    cross2 = [(2-x,x) for x in range(3)]
    for x in range(width):
        for y in range(height):
            # horizontal, vertical and both diagonal direction for part1
            part1 += sample_grid(grid, x, y, horizontal, part1_matches)
            part1 += sample_grid(grid, x, y, vertical, part1_matches)
            part1 += sample_grid(grid, x, y, diagonal1, part1_matches)
            part1 += sample_grid(grid, x, y, diagonal2, part1_matches)
            # both parts of the x must eval to 1 for part2 
            a = sample_grid(grid, x, y, cross1, part2_matches)
            b = sample_grid(grid, x, y, cross2, part2_matches)
            if a+b == 2: part2 += (a+b)//2
    print("Part 1:", part1)
    print("Part 2:", part2)
    