
import src.util as util
import math

# number of digits of x in base 10
def digit_len(x): return int(math.floor(math.log10(x))) + 1

# append the digits of y to x in base 10
def num_append(x,y): return x*(10**digit_len(y)) + y

# return digits of x in base_n, padded to required_len with zeros
# digits may be in reverse order, which doesn't matter for this application
def base_n_digits(x, n, required_len):
    digits = []
    while x > 0:
        digits.append(x % n)
        x -= (x % n)
        x //= n
    while len(digits) < required_len:
        digits.append(0)
    return digits

def day7(lines):
    part1 = 0
    part2 = 0
    for line in lines:
        vals = util.numbers_in_string(line)
        test_value = util.first(vals)
        nums = vals[1:]
        n_operators = len(nums) - 1
        valid = False
        # try all combinations of the operators +,* until a match is found,
        # iterating using a counter in base 2
        for i in range(2**n_operators):
            base_2_digits = base_n_digits(i,2,n_operators)
            total = nums[0]
            for j in range(n_operators):
                match base_2_digits[j]:
                    case 0:
                        total += nums[j+1]
                    case 1:
                        total *= nums[j+1]
            if total == test_value:
                part1 += test_value
                part2 += test_value
                valid = True
                break
        # if not already proven valid, try all combinations of the operators 
        # +,*,|| until a match is found, iterating using a counter in base 3
        if not valid:
            for i in range(3**n_operators):
                base_3_digits = base_n_digits(i,3,n_operators)
                total = nums[0]
                for j in range(n_operators):
                    match base_3_digits[j]:
                        case 0:
                            total += nums[j+1]
                        case 1:
                            total *= nums[j+1]
                        case 2:
                            total = num_append(total, nums[j+1])
                if total == test_value:
                    part2 += test_value
                    break
    print("Part 1:", part1)
    print("Part 2:", part2)
    