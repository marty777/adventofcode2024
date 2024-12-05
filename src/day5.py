
import src.util as util
from collections import defaultdict

def day5(lines):
    part1 = 0
    part2 = 0
    # Break the input lines into sections on blank lines
    sections = util.sections(lines)
    # Parse the rules into dictionaries of forward and backward rules
    forward_rules = defaultdict(list)
    backward_rules = defaultdict(list)
    for line in sections[0]:
        vals = util.numbers_in_string(line)
        forward_rules[vals[0]].append(vals[1])
        backward_rules[vals[1]].append(vals[0])
    # Parse the update lists
    updates = []
    for line in sections[1]:
        vals = util.numbers_in_string(line)
        updates.append(vals)
    # Part 1 - Validate each update by checking that no forward or backward 
    # rules are broken. Also collect any incorrect updates for part 2
    incorrects = []
    for update in updates:
        good = True
        for i in range(len(update)):
            page = update[i]
            for j in range(i+1, len(update)):
                if update[j] in backward_rules[page] or page in forward_rules[update[j]]:
                    good = False
                    break
            if not good:
                break
        if good:
            part1 += update[len(update)//2] # middle item
        else:
            incorrects.append(update)
    # Part 2 - For each item in an incorrect update, create a new list and find 
    # the correct position to insert each item based on the the forward and 
    # backward rules
    for incorrect in incorrects:
        correct = []
        for i in range(len(incorrect)):
            page = incorrect[i]
            # If the correct list is empty, insert the first item and continue
            if len(correct) == 0:
                correct.append(page)
                continue
            # Test each possible insertion position
            inserted = False
            for j in range(len(correct)): # prospective insert at index j
                good = True
                # check previous elements
                for k in range(0, j):
                    if correct[k] in forward_rules[page] or page in backward_rules[correct[k]]:
                        good = False
                        break
                if not good:
                    break
                # check subsequent elements
                for k in range(j, len(correct)):
                     if correct[k] in backward_rules[page] or page in forward_rules[correct[k]]:
                        good = False
                        break
                if good:
                    correct.insert(j, page)
                    inserted = True
                    break
            # If a valid position was not found at any existing index, insert 
            # at the end of the list
            if not inserted:
                correct.append(page)
        part2 += correct[len(correct)//2]

    print("Part 1:", part1)
    print("Part 2:", part2)
    