
import src.util as util
import numpy as np

def day13(lines):
    part1 = 0
    part2 = 0
    # split the input into sections on blank lines
    sections = util.sections(lines)
    for s in sections:
        AX, AY = util.numbers_in_string(s[0])
        BX, BY = util.numbers_in_string(s[1])
        prizeX_1, prizeY_1 = util.numbers_in_string(s[2])
        prizeX_2 = prizeX_1 + 10000000000000
        prizeY_2 = prizeY_1 + 10000000000000

        # Solve the system of linear equations for A and B, or rather have 
        # numpy do it for us, by inverting the [A,B] matrix
        AB_matrix = np.array([ [AX, BX], 
                               [AY, BY] ])
        # Added for safety, but all of the input systems of equations have 
        # invertible matrices
        try:
            AB_inverse = np.linalg.inv(AB_matrix)
        except:
            continue
        # Part 1: Calculate an integer A,B that satisfy the system of equations 
        # resulting in the prize coords.
        prize_vector1 = np.array([[prizeX_1], 
                                 [prizeY_1]])
        AB_vector1 = np.matmul(AB_inverse, prize_vector1)
        A1 = int(round(AB_vector1[0][0]))
        B1 = int(round(AB_vector1[1][0]))
        # Verify the integer system works, and add it to the part 1 token cost
        # if so
        if AX * A1 + BX * B1 == prizeX_1 and AY * A1 + BY * B1  == prizeY_1: 
            part1 += 3 * A1  + 1 * B1
        
        # Part 2: Calculate an integer A,B that satisfy the system of equations 
        # resulting in the extended prize coords.
        prize_vector2 = np.array([[prizeX_2], 
                                 [prizeY_2]])
        AB_vector2 = np.matmul(AB_inverse, prize_vector2)
        A2 = int(round(AB_vector2[0][0]))
        B2 = int(round(AB_vector2[1][0]))
        # Verify the integer system works, and add it to the part 1 token cost
        # if so
        if AX * A2 + BX * B2 == prizeX_2 and AY * A2 + BY * B2  == prizeY_2: 
            part2 += 3 * A2  + 1 * B2

    print("Part 1:", part1)
    print("Part 2:", part2)
    