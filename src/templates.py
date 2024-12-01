
# Basic templates for likely functions and structures

from copy import deepcopy

# Note - try out networkx for graph traversal. They should have dijkstra and A*
class DijkstraNode:
    def __init__(self, pos, dist, moves):
        self.pos = pos
        self.dist = dist
        self.moves = moves

#requires from copy import deepcopy
def dijkstra(graph, src, dst):
    all_edges_equal_weight = True
    seen = {}
    queue = []
    queue_next = []
    queue_next.append(DijkstraNode(src.pos, 0, []))
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            # early exit on the first node that matches dst is only valid for a graph where all edges have equal weight
            if node.pos == dst:
                if all_edges_equal_weight:
                    return (node.dist, node.moves)
            if node.pos in seen and node.dist >= seen[node.pos][0]:
                continue
            seen[node.pos] = (node.dist, node.moves)
            # Moves and updates dependant to problem type, basics given here
            for move in graph.next(node.pos):
                next_node = deepcopy(node)
                next_node.moves.append(move)
                next_node.dist += move.dist
                next_node.pos = move.result
                if seen[next_node.pos] <= next_node.dist:
                    continue
                queue_next.append(next_node)
    return seen[dst]
            