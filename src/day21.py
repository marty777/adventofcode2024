
import src.util as util
from dataclasses import dataclass

DIRECTIONS = util.arrow_dirs()

@dataclass
class DijkstraNode:
    pos: tuple
    dist: int
    path: str

# Return all button sequences that navigate from src_button to dst_button 
# with minimal length
def button_dijkstra(buttons, src_button, dst_button):
    inverse_buttons = {}
    for k in buttons:
        inverse_buttons[buttons[k]] = k
    seen = {}
    queue = []
    bests = []
    queue_next = []
    queue_next.append(DijkstraNode(buttons[src_button], 0, ''))
    while len(queue_next) > 0:
        queue = queue_next
        queue_next = []
        while len(queue) > 0:
            node = queue.pop()
            if node.pos == buttons[dst_button]:
                node.path += 'A'
                node.dist += 1
                if len(bests) == 0 or bests[0].dist == node.dist:
                    bests.append(node)
                elif bests[0].dist > node.dist:
                    bests.clear()
                    bests.append(node)
                continue
            if node.pos in seen and node.dist > seen[node.pos]:
                continue
            seen[node.pos] = node.dist
            for d in DIRECTIONS:
                next_pos = util.coord_sum(node.pos, DIRECTIONS[d])
                next_dist = node.dist + 1
                if next_pos not in inverse_buttons:
                    continue
                next_node = DijkstraNode(next_pos, next_dist, node.path+d)
                queue_next.append(next_node)
    final = []
    for b in bests:
        final.append(b.path)
    return final

# Find the length of a minimal number of numpad button presses at the specified 
# depth needed to produce the given code
def arrowpad_recurser(code, depth, transition_cache, replacement_cache):
    if (code, depth) in replacement_cache:
        return replacement_cache[(code, depth)]
    if depth == 0:
        return len(code)
    total = 0
    for i in range(len(code)):
        if i == 0:
            replacements = transition_cache[('A', code[i])]
        else:
            replacements = transition_cache[(code[i-1], code[i])]
        min_replacement = -1
        for r in replacements:
            replacement_size = arrowpad_recurser(r, depth - 1, transition_cache, replacement_cache)
            if min_replacement == -1 or min_replacement > replacement_size:
                min_replacement = replacement_size
        total += min_replacement   
    replacement_cache[(code, depth)] = total
    return replacement_cache[(code, depth)]


# Find all possible arrow button presses for the given numpad code of minimal 
# length
def numpad_code_to_arrow_presses(code, arrow_button_cache):
    result_set = set()
    for option in arrow_button_cache[('A', code[0])]:
        code_composer(code, 0, option, arrow_button_cache, result_set)
    return result_set

# Recursively explore possible mappings of arrow button sequences to numpad 
# button presses
def code_composer(code, position, partial, transition_cache, result_set):
    if position == len(code) - 1:
        result_set.add(partial)
    else:
        for option in transition_cache[(code[position], code[position+1])]:
            code_composer(code, position+1, partial + option, transition_cache, result_set)

# Find the length of a minimal mapping for each given numpad code through
# depth levels of arrowpads.
def dialer(codes, depth):
    # Define button layouts
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    numpad_buttons = {'0': (1,3), 'A':(2,3), '1':(0,2), '2': (1,2), '3': (2,2), '4': (0,1), '5': (1,1), '6': (2,1), '7': (0,0), '8': (1,0), '9': (2,0)}
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    arrowpad_buttons = {'^':(1,0), 'A':(2,0), '<':(0,1), 'v': (1,1), '>': (2,1)}
    # Build lookup of moves between arrowpad buttons
    arrowpad_moves = {}
    for button1 in arrowpad_buttons:
        for button2 in arrowpad_buttons:
            arrowpad_moves[(button1, button2)] = button_dijkstra(arrowpad_buttons, button1, button2)
    # Build lookup of moves between numpad buttons
    numpad_moves = {}
    for button1 in numpad_buttons:
        for button2 in numpad_buttons:
            numpad_moves[(button1, button2)] = button_dijkstra(numpad_buttons, button1, button2)
    # For each code, recursively find the length of a minimal expansion to the 
    # specified number of arrowpad levels, multiply by the numeric value and 
    # add to the total
    total = 0
    recursion_cache = {}
    for code in codes:
        code_val = util.numbers_in_string(code)[0]
        initial_replacements = numpad_code_to_arrow_presses(code, numpad_moves)
        best_expanded_len = -1
        for replacement in initial_replacements:
            expanded_len = arrowpad_recurser(replacement, depth, arrowpad_moves, recursion_cache)
            if best_expanded_len == -1 or expanded_len < best_expanded_len:
                best_expanded_len = expanded_len
        total += code_val * best_expanded_len
    return total
    
def day21(lines):
    print("Part 1:", dialer(lines, 2))
    print("Part 2:", dialer(lines, 25))
    