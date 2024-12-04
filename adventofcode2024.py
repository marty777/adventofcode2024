import os.path
import argparse
import requests
from dataclasses import dataclass
import json
from datetime import datetime

from src.day1 import day1
from src.day2 import day2
from src.day3 import day3
from src.day4 import day4

config_path = "./config.json"
session_key_key = 'session_key'
data_dir_path_key = 'data_dir_path'
default_data_dir_path = './data/day{day}'
default_input_file = "input.txt"
fetch_user_agent = 'Advent of Code input fetcher by martin.thorne@gmail.com'
fetch_url_format = "https://adventofcode.com/{year}/day/{day}/input"

@dataclass
class Config:
    session_key: str
    data_dir_path: str

def read_config():
    # setup config file if not present
    if not os.path.isfile(config_path):
        config_settings = {session_key_key: '', data_dir_path_key: default_data_dir_path}
        print('Setting up configuration...')
        session_key = input("Enter an Advent of Code session key (optional):")
        session_key = session_key.strip()
        if len(session_key) != 128:
            session_key = ''
        config_settings[session_key_key] = session_key
        try:
            json_object = json.dumps(config_settings, indent=4)
            with open(config_path, "w") as config_f:
                config_f.write(json_object)
            print(f"A configuration file has been created at {config_path}")
        except Exception as ex:
            print(f"An exception occured while setting up {config_path}: {ex}")
    try:
        with open(config_path) as f:
            config = json.load(f)
            session_key = config["session_key"]
            data_dir_path = config["data_dir_path"]
            return Config(session_key, data_dir_path)
    except Exception as ex:
        print("Unable to read config at path {}: {}".format(config_path, ex))
        return False

def fetch_input(day, year, session_key, data_path_string):
    import_dir_path = data_path_string.format(day=day)
    import_file_path = os.path.join(import_dir_path, default_input_file)
    # Do not re-download input file if already present
    if os.path.isfile(import_file_path):
        return import_file_path
    if session_key is None or len(session_key) == 0:
        print(f"Advent of code session key not set in {config_path}. Input file will not be downloaded")
        return False
    # Create data directory for the day if not present
    if not os.path.isdir(import_dir_path):
        try:
            os.mkdir(import_dir_path)
        except Exception as ex:
            print("Could not create directory at {}: {}".format(import_dir_path, ex))
            return False 
        print("Created directory at {}".format(import_dir_path))
    # Download the input file
    try:
        cookies = {'session': session_key}
        headers = {'User-Agent': fetch_user_agent}
        response = requests.get(fetch_url_format.format(year=year, day=day), cookies=cookies, headers=headers)
        if response.status_code != 200:
            print(f"Site returned status code {response.status_code}: {response.content}")
            return False

        content = response.content
        with open(import_file_path, 'wb') as f:
            f.write(content)
        print("Input downloaded to {}".format(import_file_path))
        return import_file_path
    except Exception as ex:
        print("Unable to download input: {}".format(ex))
        return False 

def main():
    year = 2024
    days = {
        1:day1,
        2:day2,
        3:day3,
        4:day4,
    }
    config = read_config()
    if config == False:
        return
    input_example = config.data_dir_path.format(day='#') + '/' + default_input_file
    parser = argparse.ArgumentParser(prog='adventofcode2024')
    parser.add_argument('day', help=f'The Advent of Code day # to run (1-{len(days)})', type=int)
    parser.add_argument('-f', '--file', help=f'Input file. If not specified, the file {input_example} will be run', type=str)
    args = parser.parse_args()
    day = args.day
    file_path = args.file
    if day < 1 or day > len(days):
        print(f"Available days are 1 to {len(days)}")
        return
    if file_path is None:
        if config.data_dir_path is None or config.data_dir_path == '':
            print(f"data_dir_path may not be set in {config_path} and default input files cannot be used. Set a data_dir_path or pass --file /path/to/input.txt")
            return 
        file_path = fetch_input(day, year, config.session_key, config.data_dir_path)
        if file_path == False:
            print(f"Input file for day {day} could not be found. Pass -f /path/to/input.txt to run.")
            return

    print('''   ___     __              __         ___  _____        __      _  ___ ____
  / _ |___/ /  _____ ___  / /_  ___  / _/ / ___/__  ___/ /__   ( )|_  / / /
 / __ / _  / |/ / -_) _ \/ __/ / _ \/ _/ / /__/ _ \/ _  / -_)  |// __/_  _/
/_/ |_\_,_/|___/\__/_//_/\__/  \___/_/   \___/\___/\_,_/\__/    /____//_/  
''')    
    
    print("                              --- Day %d ---" % day)
    print(f"Input file: {file_path}")
    lines = []
    try:
        f = open(file_path, "r")
        lines = f.read().splitlines()
        f.close()
    except Exception as e:
        print(e)
        return 
    start = datetime.now()
    days[day](lines)
    end = datetime.now()
    diff = end - start
    if diff.seconds == 0 and diff.microseconds < 1000:
        print("Completed in %d μs" % diff.microseconds)
    else:
        print("Completed in %d ms" % ((diff.microseconds/1000) + (1000 * diff.seconds)))
if __name__ == "__main__":
    main()

