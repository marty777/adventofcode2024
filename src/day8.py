
import src.util as util
from collections import defaultdict

# test if a coord is outside the grid
def outside(width, height, coord):
    return coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height

# Used for debugging, I'm keeping it around
def print_grid(grid, width, height, antinodes):
    for y in range(width):
        for x in range(height):
            if (x,y) in antinodes:
                print("#", end='')
            else:
                print(grid[(x,y)], end='')
        print()

def day8(lines):
    # read the grid as a defaultdict and dimensions
    grid, width, height = util.read_grid_dict(lines)
    # find all antannae, indexed by symbol
    antennae = defaultdict(set)
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] != '.':
                antennae[grid[(x,y)]].add((x,y))
    
    # using sets to omit any duplicate coordinates produced
    part1_antinodes = set()
    part2_antinodes = set()

    # part 1
    for symbol in antennae:
        symbol_group = list(antennae[symbol])
        symbol_antinodes = set()
        # find antinodes between each pair of symbols
        for i in range(len(symbol_group)):
            for j in range(i+1,len(symbol_group)):
                # determine rise and run
                delta_x = symbol_group[i][0] - symbol_group[j][0]
                delta_y = symbol_group[i][1] - symbol_group[j][1]
                # for each antenna pair antinodes occur at the same distance in
                # x,y as the opposite antenna
                antinode1 = (symbol_group[i][0] + delta_x, symbol_group[i][1] + delta_y)
                antinode2 = (symbol_group[j][0] - delta_x, symbol_group[j][1] - delta_y)
                # only add to the set if within the bounds of the grid
                if not outside(width, height, antinode1): symbol_antinodes.add(antinode1) 
                if not outside(width, height, antinode2): symbol_antinodes.add(antinode2) 
        # add all antinodes for this symbol to the main part 1 set
        part1_antinodes.update(symbol_antinodes)

    # part 2
    for symbol in antennae:
        symbol_group = list(antennae[symbol])
        symbol_antinodes = set() 
        # find antinodes between each pair of symbols
        for i in range(len(symbol_group)):
            for j in range(i+1,len(symbol_group)):
                delta_x = symbol_group[i][0] - symbol_group[j][0]
                delta_y = symbol_group[i][1] - symbol_group[j][1]
                # my input contains no perfectly horizontal or vertical antenna 
                # alignments, but this should handle them.
                if delta_x == 0:
                    for y in range(0,height):
                        symbol_antinodes.add((symbol_group[i][0], y))
                elif delta_y == 0:
                    for x in range(0,width):
                        symbol_antinodes.add((x, symbol_group[i][1]))
                else:
                    # advance across the grid by delta_x and delta_y in either 
                    # direction until outside the bounds. source antennae will
                    # necessarily contain antinodes
                    k = 0
                    while True:
                        next = (symbol_group[i][0] + delta_x*k, symbol_group[i][1] + delta_y*k)
                        if outside(width, height, next):
                            break
                        symbol_antinodes.add(next)
                        k += 1
                    k = -1
                    while True:
                        next = (symbol_group[i][0] + delta_x*k, symbol_group[i][1] + delta_y*k)
                        if outside(width, height, next):
                            break
                        symbol_antinodes.add(next)
                        k -= 1
        part2_antinodes.update(symbol_antinodes)

    print("Part 1:", len(part1_antinodes))
    print("Part 2:", len(part2_antinodes))
