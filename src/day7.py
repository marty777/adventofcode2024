
import src.util as util
import math

# number of digits of x in base 10
def digit_len(x): return int(math.floor(math.log10(x))) + 1

# test if x ends with the digits of y in base 10
def ends_with(x,y):
    if x < y: return False
    # I guess this works
    return (x - y) % (10**digit_len(y)) == 0

def remove_end(x,y):
    assert ends_with(x,y), "incorrect use of remove_end x {} y {}".format(x,y)
    return (x - y)//(10**digit_len(y))

# recursively search possible combinations of operators from right to left, 
# performing the inverse of each operation and ruling out any branches where 
# multiplication or appending (optional) makes the test value impossible to 
# reach. Recursion returns true if any branch is sucessful at reaching the test
# value
def operator_dfs(test_value, terms, include_append = False):
    if len(terms) == 1:
        return test_value == terms[0]
    x = terms[-1]
    remaining_terms = terms[:-1]
    # multiplication branch  
    # the test value must be divisible by x
    # if so, recurse on test_value//x
    if test_value % x == 0:
        if operator_dfs(test_value // x, remaining_terms, include_append): return True
    # append branch
    # the test value must end with x
    # if so, recurse on test_value with x removed
    if include_append and ends_with(test_value, x): 
        if operator_dfs(remove_end(test_value, x), remaining_terms, include_append): return True
    # addition branch
    # recurse on test_value - x
    if operator_dfs(test_value - x, remaining_terms, include_append): return True
    return False

def day7(lines):
    part1 = 0
    part2 = 0
    for line in lines:
        vals = util.numbers_in_string(line)
        test_value = util.first(vals)
        nums = vals[1:]
        if operator_dfs(test_value, nums, False):
            part1 += test_value
            part2 += test_value
        elif operator_dfs(test_value, nums, True):
            part2 += test_value
    print("Part 1:", part1)
    print("Part 2:", part2)
