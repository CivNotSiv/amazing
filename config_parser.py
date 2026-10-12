from typing import Dict
from pydantic import (BaseModel, ConfigDict, Field, ValidationError,
                      field_validator, model_validator)


class ConfigError(Exception):
    """Raised for any problem with the configuration file."""
    pass


class MazeConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')
    width: int = Field(alias="WIDTH", gt=0)
    height: int = Field(alias="HEIGHT", gt=0)
    entry: tuple[int, int] = Field(alias="ENTRY")
    exit_pos: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE", min_length=4)
    perfect: bool = Field(alias="PERFECT")
    seed: int | None = Field(default=None, alias="SEED")
    gen_algo: str | None = Field(default=None, alias="GENERATOR")
    solve_algo: str | None = Field(default=None, alias="SOLVER")

    @field_validator("entry", "exit_pos", mode="before")
    @classmethod
    def get_tuple(cls, value: object) -> object:
        """
        Creates a tuple for pydantic to use to initialize the field.
        Pydantic is unable to do this by itself.
        """
        if isinstance(value, str):
            parts = [p.strip() for p in value.split(",")]
            if len(parts) != 2:
                raise ValueError(f"expected 'x,y', got '{value}'")
            return tuple(parts)
        return value

    @field_validator("perfect", mode="before")
    @classmethod
    def bool_validation(cls, value: object) -> object:
        """
        Validates if the bool given for 'PERFECT' is an actual bool.
        Pydantic considers 'true', 'false', '0' and '1' as bools and this
        functionality is not intended for our program.
        """
        if value not in ("True", "False"):
            raise ValueError(f"expected bool, got '{value}'")
        return value == "True"

    @model_validator(mode="after")
    def check_cells(self) -> "MazeConfig":
        """
        Checks if the locations of the cells of ENTRY and EXIT are valid within
        the parameters of the maze. It also checks for if the ENTRY and EXIT
        are on the same cell which should not be possible.
        """
        for name, (x, y) in (("ENTRY", self.entry), ("EXIT", self.exit_pos)):
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} {x},{y} is outside the "
                                 f"{self.width}x{self.height} maze")
            if self.entry == self.exit_pos:
                raise ValueError("ENTRY and EXIT must be different cells")
            return self
        return self


def _read_pairs(file_name: str) -> Dict[str, str]:
    """
    This reads the KEY=VALUE lines within the config.txt file.
    It also makes sure that the lines are pre-validated for pydantic to use.
    """
    keywords = (f.alias for f in MazeConfig.model_fields.values())
    pairs: Dict[str, str] = {}
    try:
        with open(file_name) as file:
            lines = file.readlines()
    except OSError as e:
        raise ConfigError(f"cannot read '{file_name}': {e}")
    except UnicodeDecodeError:
        raise ConfigError(f"'{file_name}' is not a valid text file")
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"Line {n}: missing '=' in {line}")
        key, value = (s.strip() for s in line.split("=", 1))
        if key not in keywords:
            raise ConfigError(f"line {n}: unknown key '{key}'")
        if key in pairs:
            raise ConfigError(f"line {n}: duplicate key '{key}'")
        pairs[key] = value
    return pairs


def _format_errors(exc: ValidationError) -> str:
    """
    This function formats the errors caught by ConfigError and creates
    a representable string that will be printed after catching all errors
    during the parsing of the config.txt file.
    """
    messages = []
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"])
        msg = err["msg"].removeprefix("Value Error, ")
        if err["type"] == "missing":
            msg = "mandatory key is missing"
        messages.append(f"{field}: {msg}" if field else msg)
    return (";\n".join(messages))


def parse_config(file_name: str) -> MazeConfig:
    """
    This is the actual function that gets the parsed config. This function is
    called in the main file to retrieve the MazeConfig.
    """
    pairs = _read_pairs(file_name)
    try:
        return MazeConfig.model_validate(pairs)
    except ValidationError as e:
        raise ConfigError(_format_errors(e)) from None


if __name__ == "__main__":
    try:
        maze_config = parse_config("config.txt")
    except ConfigError as e:
        print(e)
        exit()
    print(maze_config)
