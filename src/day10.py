
import src.util as util

DIRECTIONS = util.adjacency_4()

# recursive DFS to explore all paths through available edges, recording 
# distinct destinations and paths reaching a destination
def dfs(graph, path, full_paths, destinations):
    # I'm sure there's a way to do tuples of tuples, but paths are currently 
    # recorded as alternating x and y coords. Tuples are preferred for paths
    # because they can be hashed, allowing duplicates to be omitted quickly
    pos = (path[-2], path[-1])
    if graph[pos] == 9:
        destinations.add(pos)
        full_paths.add(path)
        return
    for d in DIRECTIONS:
        next_pos = util.coord_sum(pos, d)
        if graph[next_pos] == graph[pos] + 1:
            next_path = path + (next_pos)
            dfs(graph, next_path, full_paths, destinations)

def day10(lines):
    part1 = 0
    part2 = 0
    
    # read the grid and dimensions as a defaultdict indexed by tuple (x,y)
    grid, _, _ = util.read_grid_dict(lines)
    
    # find all trailheads
    trailheads = set()
    for k in grid:
        grid[k] = int(grid[k])
        if grid[k] == 0:
            trailheads.add(k)

    # evaluate each trailhead for destinations and distinct paths reaching a 
    # trailhead
    for t in trailheads:
        destinations = set()
        full_paths = set()
        dfs(grid, (t), full_paths, destinations)
        part1 += len(destinations)
        part2 += len(full_paths)

    print("Part 1:", part1)
    print("Part 2:", part2)
    