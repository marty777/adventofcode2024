
import src.util as util

def report_safe(report):
    delta = list(map(lambda x, y: x - y, report[1:], report[:-1]))
    decrease = list(filter(lambda x: x < 0, delta))
    increase = list(filter(lambda x: x >= 0, delta))
    wrong = list(filter(lambda x: abs(x) > 3 or x == 0, delta))
    return len(wrong) == 0 and (len(decrease) == 0 or len(increase) == 0)

def day2(lines):
    part1 = 0
    part2 = 0
    for line in lines:
        report = util.numbers_in_string(line)
        if report_safe(report): part1 += 1
        for i in range(len(report)):
            test_report = report[:i] + report[i+1:]
            if report_safe(test_report):
                part2 += 1
                break
    print("Part 1:", part1)
    print("Part 2:", part2)
