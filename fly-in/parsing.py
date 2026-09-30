from pathlib import Path

from .errors import FlyInError
from .network import Map

class MapParser:
    def __init__(self, map_path: Path) -> None:
        self.map_path = map_path
        self.settings = {}

    def read_map(self) -> Map:
        try:
            with open(self.map_path, "r") as file:
                data = file.read()
        except OSError as e:
            raise FlyInError(f"{self.map_path}: Invalid path for map."
                             f" '{e.strerror}'") from e

        for line_nb, line in enumerate(data.splitlines(), start=1):
            if line.startswith('#'):
                continue
            if line.strip():
                try:
                    setting = line.partition(':')
                    settings[setting[0]] = setting[2].strip('\n')
                except ValueError as e:
                    raise FlyInError(f"'{line}': Invalid setting for map "
                                     f"creation.")

    def _parse_line(self) 



        # Loop over the lines with enumerate
        # Strip each line for blanks or comments
        # Look for prefix :
