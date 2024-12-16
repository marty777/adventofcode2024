
import src.util as util
from collections import defaultdict
from dataclasses import dataclass
from copy import deepcopy
from bisect import insort, bisect

DIRECTIONS = util.arrow_dirs()
TURNS = {'^': ['<','>'],'>': ['^','v'],'v': ['<','>'], '<': ['^','v']}

@dataclass
class DijkstraNode:
    pos: tuple
    dir: str
    dist: int
    def reverse_dir(self):
        match self.dir:
            case '^': return 'v'
            case '>': return '<'
            case 'v': return '^'
            case '<': return '>'

def dijkstra(graph, src, dst):
    # Part 1: Find a lowest cost route from src to dst
    seen = {}
    best = None
    queue = []
    queue_next = []
    queue_next.append(DijkstraNode(src, '>', 0))
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            # If the destination is reached, update the best value
            if node.pos == dst:
                if best is None or best > node.dist:
                    seen[(node.pos, node.dir)] = node.dist
                    best = node.dist
                continue
            # If this position and direction have been reached with lower cost,
            # do not advance this node
            if (node.pos, node.dir) in seen and node.dist >= seen[(node.pos, node.dir)]:
                continue
            seen[(node.pos, node.dir)] = node.dist
            # Try the forward move
            forward = util.coord_sum(node.pos, DIRECTIONS[node.dir])
            if graph[forward] != '#':
                next_node = deepcopy(node)
                next_node.dist += 1
                next_node.pos = forward
                queue_next.append(next_node)
            # Try available 90 degree turns
            for turn in TURNS[node.dir]:
                # Skip trying to turn into a wall
                if graph[util.coord_sum(node.pos, DIRECTIONS[turn])] != '#':
                    next_node = deepcopy(node)
                    next_node.dir = turn
                    next_node.dist += 1000
                    queue_next.append(next_node)

    # Part 2: Having reached the dst and knowing the lowest cost, trace 
    # positions back through the seen cache to the src, subtracting costs and
    # avoiding moves that the seen cache does not have or has at a different 
    # cost
    best_positions = set()
    queue = []
    queue_next = []
    # Two possible starting directions from the dst node: west and south
    queue_next.append(DijkstraNode(dst,'<', best))
    queue_next.append(DijkstraNode(dst,'v', best))
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            # If we've reached the start facing the opposite of the starting 
            # direction
            if node.pos == src and node.dir == '<':
                best_positions.add(node.pos)
                continue
            node_reverse = node.reverse_dir()
            # If no best route reached this position or with this cost, do not 
            # advance this node
            if (node.pos, node_reverse) not in seen or node.dist != seen[(node.pos, node_reverse)]:
                continue
            best_positions.add(node.pos)
            # Try forward
            forward = util.coord_sum(node.pos, DIRECTIONS[node.dir])
            if graph[forward] != '#':
                next_node = deepcopy(node)
                next_node.dist -= 1
                next_node.pos = forward
                queue_next.append(next_node)
            for turn in TURNS[node.dir]:
                # Skip trying to turn into a wall
                if graph[util.coord_sum(node.pos, DIRECTIONS[turn])] != '#':
                    next_node = deepcopy(node)
                    next_node.dir = turn
                    next_node.dist -= 1000
                    queue_next.append(next_node)
    return best, len(best_positions)

def day16(lines):
    # Read the grid and dimensions as a defaultdict indexed by tuple (x,y)
    grid, width, height = util.read_grid_dict(lines)
    # Find the start and end positions
    start = None
    end = None
    for x in range(width):
        for y in range(height):
            if grid[(x,y)] == 'S':
                start = (x,y)
                grid[(x,y)] = '.'
            elif grid[(x,y)] == 'E':
                end = (x,y)
                grid[(x,y)] = '.'

    part1, part2 = dijkstra(grid, start, end)
    print("Part 1:", part1)
    print("Part 2:", part2)
    