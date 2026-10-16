import sys
from src import generate, UserInterface, parse_config, ConfigError

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Excepted input: python3 ./a_maze_ing.py <config.txt>")
    try:
        config = parse_config(sys.argv[1])
    except ConfigError as e:
        sys.exit(str(e))
    maze = generate((config.width, config.height), config.seed,
                    config.perfect, None, list((config.entry, config.exit_pos)))
    app = UserInterface(maze, (config.width, config.height),
                        config.seed, config.perfect,
                        list((config.entry, config.exit_pos)), None)
    app.run()
