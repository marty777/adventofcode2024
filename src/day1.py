from bisect import insort
from collections import defaultdict

def day1(lines: list[str]):
    part1 = 0
    part2 = 0
    a = []
    b = []
    b_dict = defaultdict(int)
    for i in range(len(lines)):
        # parse the line into two integers
        left,right = map(lambda x: int(x), lines[i].split())
        # insert values into lists a and b in ascending order
        insort(a, left)
        insort(b, right)
        # increment a count of value instances in the right-hand list
        b_dict[right] += 1
    for i in range(len(lines)):
        part1 += abs(a[i] - b[i])
        part2 += a[i]*b_dict[a[i]]
    print("Part 1:", part1)
    print("Part 2:", part2)
