
import src.util as util

def find_next(line, index, match_strings):
    next = -1
    for m in match_strings:
        found = line.find(m, index)
        if found != -1 and (next == -1 or found < next): next = found
    return next

def match_substr(line, index, substr):
    if index + len(substr) >= len(line): return False
    return line[index:index+len(substr)] == substr

def eval_mul(line, index, start_mul, permitted_mul_chars):
    max_end_chars = 8 # one comma, six digits, one closing bracket
    end_mul = ')'
    if index + len(start_mul) >= len(line): return False
    chars_good = True
    end_found = False
    for internal_index in range(index + len(start_mul), max(len(line), index + len(start_mul) + max_end_chars)):
        if line[internal_index] == end_mul:
            end_found = True
            break
        if not line[internal_index] in permitted_mul_chars:
            chars_good = False
            break
    if not (chars_good and end_found): return False
    nums = util.numbers_in_string(line[index:internal_index])
    if len(nums) != 2: return False
    return (util.product_list(nums), internal_index)

def day3(lines):
    part1 = 0
    part2 = 0
    start_mul = 'mul('
    do = 'do()'
    dont = 'don\'t()'
    permitted_mul_chars = ["{}".format(x) for x in util.range_i(0,9)] + [','] # [0..9,]
    mul_enabled = True
    for line in lines:
        i = 0
        while True:
            i = find_next(line, i, [start_mul, do, dont])
            if i == -1:
                break
            elif match_substr(line, i, do):
                mul_enabled = True
                i += len(do)
            elif match_substr(line, i, dont):
                mul_enabled = False
                i += len(dont)
            elif match_substr(line, i, start_mul):
                mul_result = eval_mul(line, i, start_mul, permitted_mul_chars)
                if mul_result == False:
                    i += len(start_mul)
                else:
                    part1 += mul_result[0]
                    if mul_enabled:
                        part2 += mul_result[0]
                    i = mul_result[1]
    print("Part 1:", part1)
    print("Part 2:", part2)
