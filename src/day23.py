
import src.util as util
from collections import defaultdict

from itertools import product

def day23(lines):
    part1 = 0
    part2 = 0

    # Build a lookup of all node connections from the input
    node_connections = defaultdict(set)
    for i in range(len(lines)):
        line = lines[i]
        first, second = line.split("-")
        node_connections[first].add(second)
        node_connections[second].add(first)

    # Part 1
    # Find all mutually connected groups of 3 nodes
    three_sets = set()
    for n in node_connections:
        # For the given node, find all pairs of connected nodes that are also 
        # mutually connected
        connected = list(node_connections[n])
        for node1 in connected:
            for node2 in connected:
                if node1 == node2:
                    continue
                if node2 in node_connections[node1]:
                    # Only add to three_sets if an ordering of 
                    # (n, node1, node2) not already in three_sets
                    if not any(group_order in three_sets for group_order in list(product([n, node1, node2], repeat=3))):
                        three_sets.add((n, node1, node2))
    # Count three_sets where at least one node starts with 't'
    for s in three_sets:
        if s[0].startswith('t') or s[1].startswith('t') or s[2].startswith('t'):
            part1 += 1

    # Part 2
    # Find all fully connected node groups
    big_sets = []
    found = defaultdict(bool)
    # For each node, if not already added to a fully-connected group, find all
    # fully connected members of the same group via a BFS
    for n in node_connections:
        if found[n]:
            continue
        n_set = set()
        frontier_next = list(node_connections[n])
        frontier = []
        while len(frontier_next) > 0:
            frontier = frontier_next
            frontier_next = []
            while len(frontier) > 0:
                node = frontier.pop()
                if found[node] or node in n_set:
                    continue
                in_set = True
                for n_node in n_set:
                    if n_node not in node_connections[node]:
                        in_set = False
                        break
                if in_set:
                    n_set.add(node)
                    found[node] = True
                    for node_neighbor in node_connections[node]:
                        frontier_next.append(node_neighbor)
        if len(n_set) > 0:
            big_sets.append(n_set)
    # Find the biggest fully-connected set, sort the nodes alphabetically and
    # return as a comma-separated string
    biggest_set = None
    biggest_len = -1
    for s in big_sets:
        if len(s) > biggest_len:
            biggest_len = len(s)
            biggest_set = s
    part2 = ",".join(sorted(list(biggest_set)))

    print("Part 1:", part1)
    print("Part 2:", part2)
    