import src.util as util

def day1(lines):
    part1 = 0
    part2 = 0
    a = []
    b = []
    for i in range(len(lines)):
        left,right = lines[i].split()
        a.append(int(left))
        b.append(int(right))
    a.sort()
    b.sort()
    for i in range(len(lines)):
        part1 += abs(int(a[i]) - int(b[i]))
    print("Part 1:", part1)
    for n in a:
        part2 += n*b.count(n)
    print("Part 2:", part2)
