
import src.util as util
from collections import defaultdict

# Test if a coord is outside the grid
def outside(width, height, coord):
    return coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height

def day8(lines):
    # Read the grid as a defaultdict and dimensions
    grid, width, height = util.read_grid_dict(lines)
    # Find all antannae, indexed by symbol
    antennae = defaultdict(set)
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] != '.':
                antennae[grid[(x,y)]].add((x,y))

    # Use sets to omit any duplicate coordinates produced
    part1_antinodes = set()
    part2_antinodes = set()

    for symbol in antennae:
        symbol_group = list(antennae[symbol])
        symbol_antinodes1 = set()
        symbol_antinodes2 = set()
        # Find antinodes between each pair of symbols
        for i in range(len(symbol_group)):
            for j in range(i+1,len(symbol_group)):
                # Determine rise and run
                delta_x = symbol_group[i][0] - symbol_group[j][0]
                delta_y = symbol_group[i][1] - symbol_group[j][1]
                # Part 1: For each antenna pair antinodes occur at the same 
                # distance in x,y as the opposite antenna in the opposite direction
                antinode1 = (symbol_group[i][0] + delta_x, symbol_group[i][1] + delta_y)
                antinode2 = (symbol_group[j][0] - delta_x, symbol_group[j][1] - delta_y)
                # Only add to the set if within the bounds of the grid
                if not outside(width, height, antinode1): symbol_antinodes1.add(antinode1) 
                if not outside(width, height, antinode2): symbol_antinodes1.add(antinode2) 
                # Part 2: Since delta_x and delta_y are coprime between all 
                # antenna pairs, there's no need to search for antinode 
                # positions. All antinode positions can be found by repeating 
                # the offset in the positive and negative directions within the
                # bounds of the grid, and there can be no other grid 
                # coordinates that contain antinodes for this pair of antennae.
                # The source antennae positions will necessarily have antinodes
                k = 0
                while True:
                    next = (symbol_group[i][0] + delta_x*k, symbol_group[i][1] + delta_y*k)
                    if outside(width, height, next):
                        break
                    symbol_antinodes2.add(next)
                    k += 1
                k = -1
                while True:
                    next = (symbol_group[i][0] + delta_x*k, symbol_group[i][1] + delta_y*k)
                    if outside(width, height, next):
                        break
                    symbol_antinodes2.add(next)
                    k -= 1
        # Add all part 1 and part2 antinodes for this symbol to the main sets.
        part1_antinodes.update(symbol_antinodes1)
        part2_antinodes.update(symbol_antinodes2)

    print("Part 1:", len(part1_antinodes))
    print("Part 2:", len(part2_antinodes))
