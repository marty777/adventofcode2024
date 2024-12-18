# Puzzle notes

Discussion of the solutions for puzzles completed so far. These notes contain spoilers and shouldn't be viewed until you find your own solution.

## Day 1

Puzzle page: [Day 1: Historian Hysteria](https://adventofcode.com/2024/day/1)

Code file: [day1.py](./src/day1.py)

## Day 2

Puzzle page: [Day 2: Red-Nosed Reports](https://adventofcode.com/2024/day/2)

Code file: [day2.py](./src/day2.py)

## Day 3

Puzzle page: [Day 3: Mull It Over](https://adventofcode.com/2024/day/3)

Code file: [day3.py](./src/day3.py)

<details>
<summary>Discussion</summary>

Don't be like me. Learn how to use regexes properly.
</details>

## Day 4

Puzzle page: [Day 4: Ceres Search](https://adventofcode.com/2024/day/4)

Code file: [day4.py](./src/day4.py)

<details>
<summary>Discussion</summary>

I think this can be accomplished more efficiently by finding all `X` characters and exploring the grid for neighbors in each horizontal, vertical and diagonal direction (or `A` characters, and immediate diagonal neighbors for part 2), with early termination if a non-matching character is reached.

I didn't do any of that. Instead, I just iterated over all rows and columns and used preset offset shapes for verticals, horizontals and diagonals to sample the characters at each position and shape and check for `XMAS`/`SAMX` strings (and X shapes with  `MAS`/`SAM` strings in part 2). Storing the grid as a `collections.defaultdict` indexed by `(x,y)` tuples means it's not even necessary to check bounds rigorously. The approach involves unnecessary extra work (and a hashed dictionary is necessarily slower to access than a 2D array), but the runtime cost is minimal when run on puzzle inputs and it simplifies the code substantially.
</details>

## Day 5

Puzzle page: [Day 5: Print Queue](https://adventofcode.com/2024/day/5)

Code file: [day5.py](./src/day5.py)

<details>
<summary>Discussion</summary>

It's interesting that the page ordering rules on the puzzle inputs contain cycles if the graph is mapped, but the pages of each update are carefully selected to avoid these cycles and have a correct ordering that is unambigious. Possibly this was meant as a trap for anyone who tries to obtain a full ordering of pages before evaluating the updates.

Evaluating the ordering of an update for part 1 just requires verifying that no rules are broken by the current ordering. For any applicable `first|last` orderings on the update list, no `first` pages can appear after `last` pages (and vice versa). Pre-sorting the rules into dictionaries indexed by `first` and `last` pages simplifies the code and is relatively efficient.

For part 2, I used an insertion sort of each page into a new list, where the insertion point for a page is the first index where the page would not break any ordering rules. I'm pretty sure the cost of sorting is no worse than $\mathcal{O}(n \log n)$ using this method.
</details>

## Day 6

Puzzle page: [Day 6: Guard Gallivant](https://adventofcode.com/2024/day/6)

Code file: [day6.py](./src/day6.py)

<details>
<summary>Discussion</summary>

The solution to part 2 is pretty easily found via brute force and a little waiting. There are two useful optimizations which dropped my runtime by nearly two orders of magnitude from the initial pass.

1. An obstruction must be placed somewhere in the original path of the guard in order for it to have any effect on the guard's route. Placing an obstruction anywhere on the grid that the guard does not reach in part 1 cannot create a cycle and so does not need to be simulated.
2. Rather than move the guard one space at a time in part 2, it's faster to collect a list of obstacle/obstruction positions indexed by row and column, and jump the guard to the next obstacle (or out of the grid area) in a single step. It's still simplest to move the guard one space at a time in part 1, in order to find all visited coordinates.
</details>

## Day 7

Puzzle page: [Day 7: Bridge Repair](https://adventofcode.com/2024/day/7)

Code file: [day7.py](./src/day7.py)

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
            total += term[j+1]
        else:
            total *= term[j+1]
    if total == test_value:
        part1 += test_value
        break
```

Relying on this does not offer any help in part 2, where there are $n$ ordered items with $3$ options each instead. I [initially](https://github.com/marty777/adventofcode2024/blob/d37f29fe61f25ba20d2831784ca2cbfbbf37aa95/src/day7.py) ended up with a method to extract the digits of an integer in an arbitrary base, then iterated over $0$ to $3^n - 1$ using the digits in base $3$ to brute force the part 2 solution, which completed in slow but reasonable time.

The final version of the day 7 solution switches instead to a recursive depth first search for the inverse of each operation in right-to-left order, not following branches where multiplication is ruled out by non-divisibility or where appending is ruled out by an incompatible digit ending. This drops the runtime by several orders of magnitude.</details>

## Day 8

Puzzle page: [Day 8: Resonant Collinearity](https://adventofcode.com/2024/day/8)

Code file: [day8.py](./src/day8.py)

<details>
<summary>Discussion</summary>

This ended up being oddly simple in part 2. The description of the problem indicates that any grid position that occupies a point on the line between two alike antennae forms an antinode. In the general case this is somewhat more complicated, but the puzzle input has been constructed with every pair of antennae in a group arranged such that the horizontal and vertical distances between them are *coprime*. This makes finding antinode positions trivial, since the antinodes are all at positive or negative offsets of the horizontal and vertical distances between the antennae and no other grid positions can contain antinodes.
</details>

## Day 9

Puzzle page: [Day 9: Disk Fragmenter](https://adventofcode.com/2024/day/9)

Code file: [day9.py](./src/day9.py)

<details>
<summary>Discussion</summary>

I think there are a few good approaches to this puzzle. Mine was to construct separate lists tracking file blocks and empty blocks, and progressively move the furthest right blocks into the furthest left available empty spaces as described, updating file block indexes and empty block lengths/positions as needed. The compacting process was reused in both parts of the puzzle without changes by creating multiple 1-block file blocks for each file id in part 1, allowing files to fragment, and single blocks of the specified length for each file id in part 2.
</details>

## Day 10

Puzzle page: [Day 10: Hoof It](https://adventofcode.com/2024/day/10)

Code file: [day10.py](./src/day10.py)

<details>
<summary>Discussion</summary>

A pathfinding puzzle, where I was so eager to Dijkstra's algorithm that I slapped it down before getting to part 2. Dijkstra's algorithm isn't great for finding all paths to all goals without modification, so this was hastily rewritten as a DFS instead. Part 1, asking for a score of each trailhead by how many peaks are accessible, can be solved by fully exploring the graph from each trailhead position and counting the number of distinct peaks reached by the DFS. The rating of each trailhead can be found by fully exploring the graph from each trailhead position and counting the number of times a DFS reaches a peak (each time a peak is reached it necessarily will be via a distinct path), but I also kept track of the paths of each branch in the DFS and used a set to eliminate duplicates.
</details>


## Day 11

Puzzle page: [Day 11: Plutonian Pebbles](https://adventofcode.com/2024/day/11)

Code file: [day11.py](./src/day11.py)

<details>
<summary>Discussion</summary>

This is probably the first challenging puzzle of 2024 for me. My initial approach was to simulate the blinking process using linked lists to represent the stones, which have the advantage over arrays that mid-array inserts have a much lower cost. This was quite fast for part 1, blinking 25 times, but not adequate for part 2. In part 2, fully representing the list of stones would require a infeasibly large amount of memory and a great deal of time to reach blink 75.

I initially came up with a scheme to take each initial stone in the input, advance it 37 blinks, take the stone in each resulting set and advance those a further 38 blinks. While each 37-set contains $10^7$ to $10^8$ elements, there are a large number of duplicate stones across all the sets, which memoization would prevent the need to recalculate each time. I estimated this would work within a large but acceptable memory footprint, and take no more than a few hours to complete.

After starting the process, I had time to think of other approaches. I finally realized that the order of the stones, while repeatedly underlined as being important in the puzzle description, did not have an actual bearing on the part 2 answer, and so recursion could be used determine the number of stones after arbitrary numbers of blinks (up to the stack limit, anyway). Combining recursion on each starting stone with a memoizing cache of previous results for stones at various steps in the blink updates and divisions, the answer is reachable very quickly.

There's another approach spotted on the subreddit, which I like even better. Rather than relying on recursion, it takes the observation that the order of the stones doesn't matter even futher and represents stones as counts of the numbers displayed on the collection of stones in the current set. At each blink step, the counts of different numbers on each stones are updated based on the previous stone population and the division and update rules using simple arithmetic. The process runs slightly faster than the recursive approach, and uses much less memory.
</details>

## Day 12

Puzzle page: [Day 12: Garden Groups](https://adventofcode.com/2024/day/12)

Code file: [day12.py](./src/day12.py)

<details>
<summary>Discussion</summary>

The individual regions can be found on the grid easily enough using a flood-fill/BFS from each point on the grid which hasn't previously been assigned to a region.

While there's a nice shortcut for determining the perimeter length during the flood-fill (for each new plot added to the region, add 4 to the perimeter and subtract 1 for each adjacent plot in the same region) and the number of sides can be found by counting the corners of the region, I took a different approach. Once all the plots in a region have been found, repeat the following for each direction in [N,E,S,W]:

- Find all plots on a border in the selected direction. This is any plot which does not have a neighboring plot in the same region immediately in that direction.
- Collect these border plots into row lists (if direction is N/S) or column lists (if direction is E/W). Order the plots within each row/column by the orthogonal coordinate.
- Traversing over each non-empty list, add 1 side initially and add another side each time there is a discontinuity in the plots.

Collect the sum of sides over each list and direction covers all sides on the border of the region, concave or convex, internal or external. The perimeter length of the region can also be found during this process.
</details>

## Day 13

Puzzle page: [Day 13: Claw Contraption](https://adventofcode.com/2024/day/13)

Code file: [day13.py](./src/day13.py)

<details>
<summary>Discussion</summary>

Despite the misdirections about maximum button presses and minimation of costs, the puzzle gives a straightforward set of systems of linear equations. The matrices for the x and y increments of the A and B buttons are all invertible, and so each machine can be solved by inverting each matrix, multiplying by the prize x and y vector, and only returning a solution if the values of the resulting button press vector are both divisible by the determinant, forming an integer solution. I initially used [numpy](https://numpy.org/) to obtain my inverse matrices, but implementing the inverse of a 2x2 matrix directly and being careful to avoid floating point calculations was able to speed up the solution by an order of magnitude.
</details>
