
import src.util as util
from collections import defaultdict
from dataclasses import dataclass

DIRECTIONS = util.adjacency_4()

@dataclass
class DijkstraNode:
    pos: tuple
    dist: int

def dijkstra(graph, width, height, src, dst, byte_index):
    seen = {}
    queue = []
    queue_next = []
    queue_next.append(DijkstraNode(src, 0))
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            # If the destination is reached, return immediately. All edges in 
            # this graph are of equal length.
            if node.pos == dst:
                return node.dist
            # If this position and direction have been reached with lower cost,
            # do not advance this node
            if node.pos in seen and node.dist >= seen[node.pos]:
                continue
            seen[node.pos] = node.dist
            for d in DIRECTIONS:
                next_pos = util.coord_sum(node.pos, d)
                if util.outside(width, height, next_pos):
                    continue
                if graph[next_pos] != 0 and graph[next_pos] <= byte_index:
                    continue
                next_node = DijkstraNode(next_pos, node.dist+1)
                queue_next.append(next_node)
    if dst not in seen: return False
    return seen[dst]

def day18(lines):
    part1 = 0
    part2 = 0
    # Set parameters and read the grid
    width = 71
    height = 71
    fall_index = 1024
    start = (0,0)
    destination =(70,70)
    
    # Load the grid, with each falling byte marked as an integer >= 1 by index
    # and all other positions marked as 0
    grid = defaultdict(int)
    for i in range(len(lines)):
        vals = util.numbers_in_string(lines[i])
        grid[(vals[0],vals[1])] = i + 1

    # Part 1: Traverse the grid for with the bytes given by fall_index present 
    # on the grid
    part1 = dijkstra(grid, width, height, start, destination, fall_index)
   
    # Part 2: Remove bytes from the grid until the path is traversable to 
    # quickly find the answer.
    for j in range(0, len(lines)):
        fall_index = len(lines) - 1 - j
        if dijkstra(grid, width, height, start, destination, fall_index) is not False:
            part2 = lines[fall_index]
            break
    
    print("Part 1:", part1)
    print("Part 2:", part2)
    