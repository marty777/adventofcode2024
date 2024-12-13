# adventofcode2024
[Advent of Code 2024](https://adventofcode.com/2024) in Python.

## Setup

```console
$ git clone https://github.com/marty777/adventofcode2024
$ cd adventofcode2024
$ pip install requests
$ pip install argparse
$ pip install numpy
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
$ python adventofcode2024.py [-h] [-f FILE] day

positional arguments:
day                   The Advent of Code day # to run

options:
-h, --help            show this help message and exit
-f FILE, --file FILE  Input file. If not specified the file ./data/day#/input.txt will be run
```

Any input file can be passed in with the `-f` option. By default, the script expects the main input file for a puzzle day to be at the path `./data/day#/input.txt` (e.g. `./data/day1/input.txt` for day 1) and will attempt to load the input file corresponding to the day if no file is otherwise specified. The path for the default data directory can be modified in `./config.json`. If an Advent of Code session key has been configured, the input file for the day will be automatically downloaded to the default input file location if not already present.

## Example

To run day 1:

```console
$ python adventofcode2024.py -f data/day1/input.txt 1 
```

With the default data directory config setting, this is equivalent to

```console
$ python adventofcode2024.py 1
```

If an Advent of Code session key has been configured, the input file for the specified day will be automatically downloaded and saved to the expected location. If not, the `input.txt` file for the intended day should be manually saved first.
