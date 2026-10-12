import sys
from config_parser import parse_config, ConfigError
from generator import generate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Excepted input: <main.py> <config.txt>")
    try:
        config = parse_config(sys.argv[1])
    except ConfigError as e:
        exit(e)
    