
import src.util as util
from collections import defaultdict

# Perform one secret evolution step
def evolve(secret):
    result = secret * 64
    secret = secret ^ result # mix
    secret = secret % 16777216 # prune 
    result = secret // 32
    secret = secret ^ result # mix 
    secret = secret % 16777216 # prune 
    result = secret * 2048
    secret = secret ^ result # mix 
    secret = secret % 16777216 # prune 
    return secret

# Evolve the buyer's initial secret for the specified number of repetitions, 
# recording the resulting price and price change at each step
def repeat_evolve(initial, count):
    secret = initial
    deltas = []
    prices = []
    last = initial
    for i in range(count):
        secret = evolve(secret)
        deltas.append((secret % 10) - (last % 10))
        prices.append(secret % 10)
        last = secret
    return secret, deltas, prices

def day22(lines):
    part1 = 0
    part2 = -1
    sequences = defaultdict(list)
    
    for line in lines:
        vals = util.numbers_in_string(line)
        final, deltas, prices = repeat_evolve(vals[0], 2000)
        part1 += final
        # Examine all sequences of changes in this buyer's pricing (omitting
        # repeats) and record the final price associated with the sequence
        line_sequences = {}
        for j in range(3, len(deltas)):
            sequence = (deltas[j-3], deltas[j-2], deltas[j-1], deltas[j])
            if sequence in line_sequences:
                continue
            line_sequences[sequence] = prices[j]
        # Add the recorded price at the end of each of this buyer's price 
        # change sequences to a collection of common sequences between all 
        # buyers
        for sequence in line_sequences:
            sequences[sequence].append(line_sequences[sequence])
    
    # Find the sequence that will fetch the highest sum of prices across all 
    # buyers 
    for sequence in sequences:
        score = util.sum_list(sequences[sequence])
        if part2 == -1 or part2 < score:
            part2 = score
    
    print("Part 1:", part1)
    print("Part 2:", part2)
    