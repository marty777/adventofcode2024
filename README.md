# adventofcode2024
[Advent of Code 2024](https://adventofcode.com/2024) in Python.

## Configuration

```console
$ git clone https://github.com/marty777/adventofcode2024
$ cd adventofcode2024
$ python adventofcode2024.py
Setting up configuration...
Enter an Advent of Code session key (optional):
```

If an active session key for the Advent of Code website is entered it will be stored in `./config.json` and input files can be automatically downloaded and saved when a puzzle solution is run. Press enter to skip. **If a session key is entered, please make sure not to share your config file with others**.

```console
A configuration file has been created at ./config.json
usage: adventofcode2024 [-h] [-f FILE] day
adventofcode2024: error: the following arguments are required: day
```

## Usage

```console
$ adventofcode2024 [-h] [-f FILE] day

positional arguments:
day                   The Advent of Code day # to run

options:
-h, --help            show this help message and exit
-f FILE, --file FILE  Input file. If not specified the file ./data/day#/input.txt will be run
```

## Example

To run day 1:

```console
$ python adventofcode2024 -f data/day1/input.txt 1 
```

With the default data directory config setting, this is equivalent to

```console
$ python adventofcode2024 1
```

If an Advent of Code session key has been configured, the input file for the specified day will be automatically downloaded and saved to the expected location. If not, the `input.txt` file for the intended day should be manually saved first.