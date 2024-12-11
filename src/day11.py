
import src.util as util
import math

def digit_len(x): return int(math.floor(math.log10(x))) + 1

def from_digits(digits):
    total = 0
    for i in range(len(digits)):
        mul = 10**i
        total += mul*digits[len(digits) - 1 -i]
    return total

def digit_split(x):
    assert digit_len(x) % 2 == 0, "incorrect use of digit split on {}".format(x)
    digits = util.base_n_digits(x, 10, None)
    left_val = from_digits(digits[:len(digits)//2])
    right_val = from_digits(digits[len(digits)//2:])
    return left_val, right_val

# returns number of items after n blinks of x using the power of dynamic programming
def blink(x, n, cache):
    # not really useful to cache
    if n == 0:
        return 1
    # if already in cache return
    if (x,n) in cache:
        return cache[(x,n)]
    # if not in cache, recurse down until cache or n=0 case is hit
    result = 0
    if x == 0:
        result = blink(1, n - 1, cache)
    elif digit_len(x) % 2 == 0:
        left, right = digit_split(x)
        result = blink(left, n - 1, cache) + blink(right, n - 1, cache)
    else:
        result = blink(x*2024, n - 1, cache)
    # update cache
    cache[(x, n)] = result
    return result
    
def day11(lines):
    part1 = 0
    part2 = 0
    vals = util.numbers_in_string(lines[0])
    cache = {}
    for v in vals:
        part1 += blink(v, 25, cache)
        part2 += blink(v, 75, cache)    
    print("Part 1:", part1)
    print("Part 2:", part2)
