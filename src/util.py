import functools
import re
from collections import defaultdict

## General helper functions

# file helpers 

# break input lines into sections on empty lines
def sections(lines):
    result = [[]]
    for line in lines:
        if len(line) == 0:
            result.append([])
        else:
            result[-1].append(line)
    return result

# list helpers
def first(x): return x[0]
def second(x): return x[1]
def last(x): return x[-1]
def first_safe(x): 
    if x is None or len(x) < 1: return None
    return x[0]
def second_safe(x): 
    if x is None or len(x) < 2: return None
    return x[1]
def last_safe(x): 
    if x is None or len(x) < 1: return None
    return x[-1]

# range helper
def range_i(a,b): return range(a,b+1) # range inclusive

# 2D helpers
# read lines of a file and return characters as a 2d array
def read_grid(lines):
    grid = []
    for line in lines:
        grid.append([])
        for c in range(len(line)):
            grid[len(grid) - 1].append(line[c])
    return grid
# read lines of a file and return characters as a defaultdict grid, plus the width and height
def read_grid_dict(lines, default_str = '.'):
    grid = {}
    height = len(lines)
    width = len(lines[0])
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x,y)] = lines[y][x]
    return defaultdict(lambda: default_str, grid), width, height
def adjacency_4(): return [(0,-1), (1,0), (0,1), (-1,0)]
def adjacency_5(): return [(0,-1), (1,0), (0,1), (-1,0), (0,0)]
def adjacency_8(): return [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (1,1), (0,1), (1,1)]
def adjacency_9(): return [(-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0), (1,1), (0,1), (1,1)]
def coord_sum(a,b): return (a[0] + b[0], a[1] + b[1])

# sum of a list of numeric items
def sum_list(list):
    return functools.reduce(lambda x,y: x+y, list, 0)

# product of a list of numeric items
def product_list(list):
    return functools.reduce(lambda x,y: x*y, list, 1)

# find all numeric values in a string, extract them, cast to an int or float and return the list
def numbers_in_string(str):
    list = re.findall('-?\d+\.?\d*',str)
    result = []
    for item in list:
        if "." in item:
            result.append(float(item))
        else:
            result.append(int(item))
    return result

# basic Sieve of Eratosthenes. Return a list of primes up to sqrLimit
def eratosthenes(sqrLimit):
    if sqrLimit < 2:
        sqrLimit = 2
    primes = []
    sieve = [False] * sqrLimit
    increment = 2
    done = False
    while True:
        for i in range(2*increment, sqrLimit, increment):
            sieve[i] = True
        done = True
        for i in range(increment+1, sqrLimit,1):
            if not sieve[i]:
                increment = i
                done = False
                break
        if done:
            break
    for i in range(2, sqrLimit, 1):
        if not sieve[i]:
            primes.append(i)
    return primes

# this one came in useful once. return the digits of x in base n padded to the
# required length (or not, if required_len = None)
def base_n_digits(x, n, required_len = None):
    digits = []
    while x > 0:
        digits.insert(0, x % n)
        x -= (x % n)
        x //= n
    if required_len is not None:
        while len(digits) < required_len:
            digits.insert(0,0)
    return digits