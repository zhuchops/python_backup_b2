from dataclasses import dataclass

import yaml
from pathlib import Path


class MyConfig:
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def _check_dir(self, path: Path) -> bool:
        if path.exists():
            if path.is_dir():
                return True
        return False

    def read(self) -> MyConfigData:
        try:
            with open(self.path) as f:
                config = yaml.safe_load(f)
        except OSError:
            raise CantLocateFile(self.path)

        dirs = list()
        if "dirs" in config:
            dirs.extend(filter(lambda x: self._check_dir(x), config["dirs"]))
        else:
            raise NoRequiredFieldFound("dirs")

        death_delay = 0
        if "death_delay" in config:
            death_delay = config["death_delay"]
        else:
            raise NoRequiredFieldFound("death_delay")

        return MyConfigData(dirs, 0)



@dataclass
class MyConfigData:
    dirs: list[Path]
    death_delay: int

class ParsingError(Exception):
    pass

class CantLocateFile(ParsingError):
    e: str
    path: Path

    def __init__(self, path: Path) -> None:
        self.e = "No file found"
        self.path = path
        super().__init__(self.e)

class NoRequiredFieldFound(ParsingError):
    e: str
    field: str

    def __init__(self, field: str) -> None:
        self.field = field
        self.e = f"No required field {field} found"
        super().__init__(self.e)


class WrongDirectoryPath(ParsingError):
    e: str
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path
        self.e = f"Can not locate directory on {self.path}"
        super().__init__(self.e)
