
import src.util as util

# Solve the system [a_presses, b_presses] * M = [[prize_x], [prize_y]] for 
# a_presses, b_presses by inverting the matrix M for the system of linear 
# equations of the a and b buttons and multiplying by [[prize_x], [prize_y]]
def prize_solver(aX, aY, bX, bY, prizeX, prizeY):
    assert aX*bY - aY*bX != 0, "Determinant denominator is zero"
    # Build an inverse matrix of [[aX, bX], [aY, bY]] leaving the determinant 
    # multiplication for the end
    inverse_matrix = [ [bY, -bX],
                       [-aY, aX] ]
    presses_vector = [inverse_matrix[0][0] * prizeX + inverse_matrix[0][1] * prizeY, 
                      inverse_matrix[1][0] * prizeX + inverse_matrix[1][1] * prizeY]
    # Return only integer solutions
    if presses_vector[0] % (aX*bY - aY*bX) == 0 and presses_vector[1] % (aX*bY - aY*bX) == 0:
        return presses_vector[0]//(aX*bY - aY*bX), presses_vector[1]//(aX*bY - aY*bX)
    return False, False
    
def day13(lines):
    part1 = 0
    part2 = 0
    # Split the input into sections on blank lines
    sections = util.sections(lines)
    for s in sections:
        # Get parameters for the section
        AX, AY = util.numbers_in_string(s[0])
        BX, BY = util.numbers_in_string(s[1])
        prizeX_1, prizeY_1 = util.numbers_in_string(s[2])
        prizeX_2 = prizeX_1 + 10000000000000
        prizeY_2 = prizeY_1 + 10000000000000
        # Solve the systems of linear equations for part 1 and part 2 using 
        # inverse matrices, since each input system is invertible.
        a_presses1, b_presses1 = prize_solver(AX, AY, BX, BY, prizeX_1, prizeY_1)
        if a_presses1 is not False:
            part1 += 3 * a_presses1  + 1 * b_presses1
        a_presses2, b_presses2 = prize_solver(AX, AY, BX, BY, prizeX_2, prizeY_2)
        if a_presses2 is not False:
            part2 += 3 * a_presses2  + 1 * b_presses2
    print("Part 1:", part1)
    print("Part 2:", part2)
    