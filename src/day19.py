
import src.util as util
from collections import defaultdict

# Recursively find the total number of pattern combinations that can produce 
# the given towel design
def towel_designs(remaining_towel, first_color_lookup, cache):
    if remaining_towel in cache:
        return cache[remaining_towel]
    first_color = remaining_towel[0]
    total = 0
    for p in first_color_lookup[first_color]:
        if p == remaining_towel:
            total += 1
        else:
            sub_towel = remaining_towel[len(p):]
            if p + sub_towel == remaining_towel:
                total += towel_designs(sub_towel, first_color_lookup, cache)
    cache[remaining_towel] = total
    return cache[remaining_towel]

def day19(lines):
    part1 = 0
    part2 = 0    
    sections = util.sections(lines)
    patterns = sections[0][0].split(", ")
    first_color_lookup = defaultdict(set)
    cache = {}
    # Build a lookup of patterns by first color
    for p in patterns:
        first = list(p)[0]
        first_color_lookup[first].add(p)
    # Find designs for each towel given patterns via the power of dynamic 
    # programming
    for line in sections[1]:
        design_count = towel_designs(line, first_color_lookup, cache)
        if design_count > 0:
            part1 += 1
        part2 += design_count

    print("Part 1:", part1)
    print("Part 2:", part2)
    