
import src.util as util
from collections import defaultdict
from dataclasses import dataclass

DIRECTIONS = util.adjacency_4()

@dataclass
class DijkstraNode:
    pos: tuple
    dist: int

def dijkstra(graph, src, dst, cheat_mask, cheat_cutoff):
    seen = {}
    queue = []
    base_dist = None
    queue_next = []
    queue_next.append(DijkstraNode(src, 0))
    # Fully explore paths from src to dst
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            if node.pos in seen and node.dist >= seen[node.pos]:
                continue
            seen[node.pos] = node.dist
            # If the destination is reached, return immediately. All edges in 
            # this graph are of equal length.
            if node.pos == dst:
                base_dist = node.dist
                continue
            # If this position and direction have been reached with lower cost,
            # do not advance this node
            for d in DIRECTIONS:
                next_pos = util.coord_sum(node.pos, d)
                if graph[next_pos] == '#':
                    continue 
                next_node = DijkstraNode(next_pos, node.dist+1)
                queue_next.append(next_node)
    # Use the seen cache to find cheat start and end points that result in 
    # distance savings
    found_cheats = set()
    cheat_count = 0 # cheats saving at or above cheat_cutoff moves
    seen_dists = defaultdict(set)
    seen_max = seen[dst]
    for s in seen:
        seen_dists[seen[s]].add(s)
    for i in range(0, seen_max+1):
        for start_point in seen_dists[i]:
            for c in cheat_mask:
                cheat_dist = abs(c[0]) + abs(c[1])
                end_point = util.coord_sum(start_point, c)
                if end_point in seen and seen[end_point] > i + cheat_dist and (start_point, end_point) not in found_cheats and (end_point, start_point) not in found_cheats:
                    savings = (seen[end_point] - i) - cheat_dist
                    if savings >= cheat_cutoff:
                        cheat_count += 1
                    found_cheats.add((start_point, end_point))
    return cheat_count

def day20(lines):
    part1 = 0
    part2 = 0
    # Read the grid and dimensions as a defaultdict indexed by tuple (x,y)
    grid, width, height = util.read_grid_dict(lines)
    # Build offset diamonds for manhattan ranges 2 and 20
    cheat_length_part1 = 2
    manhattan_diamond_part1 = set()
    for x in range(-cheat_length_part1, cheat_length_part1+1):
        for y in range(-cheat_length_part1, cheat_length_part1+1):
            if abs(x) + abs(y) <= cheat_length_part1:
                manhattan_diamond_part1.add((x,y))
    cheat_length_part2 = 20
    manhattan_diamond_part2 = set()
    for x in range(-cheat_length_part2, cheat_length_part2+1):
        for y in range(-cheat_length_part2, cheat_length_part2+1):
            if abs(x) + abs(y) <= cheat_length_part2:
                manhattan_diamond_part2.add((x,y))
    # Find start and end coords
    start = None
    end = None
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == 'S':
                start = (x,y)
            elif grid[(x,y)] == 'E':
                end = (x,y)
            
    part1 = dijkstra(grid, start, end, manhattan_diamond_part1, 100)
    part2 = dijkstra(grid, start, end, manhattan_diamond_part2, 100)
    
    print("Part 1:", part1)
    print("Part 2:", part2)
    