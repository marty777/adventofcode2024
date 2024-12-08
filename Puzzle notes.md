# Puzzle notes

Discussion of the solutions for puzzles completed so far. These notes contain spoilers and shouldn't be viewed until you find your own solution.

## Day 3

Puzzle page: [Day 3: Mull It Over](https://adventofcode.com/2024/day/3)

Code file: [day3.py](./day3.py)

<details>
<summary>Discussion</summary>

Don't be like me. Learn how to use regexes properly.
</details>

## Day 4

Puzzle page: [Day 4: Ceres Search](https://adventofcode.com/2024/day/4)

Code file: [day4.py](./day4.py)

<details>
<summary>Discussion</summary>

I think this can be accomplished more efficiently by finding all `X` characters and exploring the grid for neighbors in each horizontal, vertical and diagonal direction (or `A` characters, and immediate diagonal neighbors for part 2), with early termination if a non-matching character is reached.

I didn't do any of that. Instead, I just iterated over all rows and columns and used preset offset shapes for verticals, horizontals and diagonals to sample the characters at each position and shape and check for `XMAS`/`SAMX` strings (and X shapes with  `MAS`/`SAM` strings in part 2). Storing the grid as a `collections.defaultdict` indexed by `(x,y)` tuples means it's not even necessary to check bounds rigorously. The approach involves unnecessary extra work (and a hashed dictionary is necessarily slower to access than a 2D array), but the runtime cost is minimal when run on puzzle inputs and it simplifies the code substantially.
</details>

## Day 5

Puzzle page: [Day 5: Ceres Search](https://adventofcode.com/2024/day/5)

Code file: [day5.py](./day5.py)

<details>
<summary>Discussion</summary>

It's interesting that the page ordering rules on the puzzle inputs contain cycles if the graph is mapped, but the pages of each update are carefully selected to avoid these cycles and have a correct ordering that is unambigious. Possibly this was meant as a trap for anyone who tries to obtain a full ordering of pages before evaluating the updates.

Evaluating the ordering of an update for part 1 just requires verifying that no rules are broken by the current ordering. For any applicable `first|last` orderings on the update list, no `first` pages can appear after `last` pages (and vice versa). Pre-sorting the rules into dictionaries indexed by `first` and `last` pages simplifies the code and is relatively efficient.

For part 2, I used an insertion sort of each page into a new list, where the insertion point for a page is the first index where the page would not break any ordering rules. I'm pretty sure the cost of sorting is no worse than $\mathcal{O}(n \log n)$ using this method.
</details>

## Day 6

Puzzle page: [Day 6: Guard Gallivant](https://adventofcode.com/2024/day/6)

Code file: [day6.py](./day6.py)

<details>
<summary>Discussion</summary>

The solution to part 2 is pretty easily found via brute force and a little waiting. There are two useful optimizations which dropped my runtime by nearly two orders of magnitude from the initial pass.

1. An obstruction must be placed somewhere in the original path of the guard in order for it to have any effect on the guard's route. Placing an obstruction anywhere on the grid that the guard does not reach in part 1 cannot create a cycle and so does not need to be simulated.
2. Rather than move the guard one space at a time in part 2, it's faster to collect a list of obstacle/obstruction positions indexed by row and column, and jump the guard to the next obstacle (or out of the grid area) in a single step. It's still simplest to move the guard one space at a time in part 1, in order to find all visited coordinates.
</details>

## Day 7

Puzzle page: [Day 7: Bridge Repair](https://adventofcode.com/2024/day/7)

Code file: [day7.py](./day7.py)

<details>
<summary>Discussion</summary>

I ran into some trouble with this. It's an easily-memorized trick that you can efficiently iterate over all combinations of $n$ ordered items with $2$ options each using the bits of integers $0$ to $2^n - 1$, which is perfect for brute forcing combinations of `+` and `*` operators in the equations for part 1 until a solution is found.

```python
# term the list of terms of the equation
# n the number of operators, i.e. len(term) - 1
for i in range(2**n):
    total = term[0]
    for j in range(n):
        option = (i >> j) & 0b1 # get the jth bit of integer i
        if option == 0:
            total += term[item+1]
        else:
            total *= term[item+1]
    if total == test_value:
        part1 += test_value
        break
```

Relying on this does not offer any help in part 2, where there are $n$ ordered items with $3$ options each instead. I [initially](https://github.com/marty777/adventofcode2024/blob/d37f29fe61f25ba20d2831784ca2cbfbbf37aa95/src/day7.py) ended up with a method to extract the digits of an integer in an arbitrary base, then iterated over $0$ to $3^n - 1$ using the digits in base $3$ to brute force the part 2 solution, which completed in slow but reasonable time.

The final version of the day 7 solution switches instead to a recursive depth first search for the inverse of each operation in right-to-left order, not following branches where multiplication is ruled out by non-divisibility or where appending is ruled out by an incompatible digit ending. This drops the runtime by several orders of magnitude.


</details>