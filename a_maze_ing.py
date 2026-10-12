import sys
from src.generator import generate
from src.algorithms.dfs_solver import dfs_solver
from src.config_parser import parse_config, ConfigError

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Excepted input: <main.py> <config.txt>")
    try:
        config = parse_config(sys.argv[1])
    except ConfigError as e:
        exit(e)
    maze = generate((config.width, config.height), config.seed,
                    config.perfect, None)
    maze = dfs_solver(maze)