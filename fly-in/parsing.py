from pathlib import Path

from .errors import FlyInError
from .network import Map

class MapParser:
    def __init__(self, map_path: Path) -> None:
        self.map_path = map_path
        self.settings = {}

        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}

    def read_map(self) -> Map:
        try:
            with open(self.map_path, "r") as file:
                data = file.read()
        except OSError as e:
            raise FlyInError(f"{self.map_path}: Invalid path for map."
                             f" '{e.strerror}'") from e

        for line_nb, line in enumerate(data.splitlines(), start=1):
            if line.strip().startswith('#'):
                continue
            if line.strip():
                self._parse_line(line)

    def _parse_line(self, line: str) -> None:
        setting = line.partition(':')
        if not setting[1]:
            raise FlyInError(f"Wrong syntax: '{line}' missing ':'.")
        if setting[0].strip() != "nb_drones" and not self.nb_drones:
            raise FlyInError("Missing nb_drones assignement.")
        match setting[0].strip():
            case "nb_drones":
                if not self.nb_drones:
                    self._parse_nb_drones(setting[2])
                else:
                    raise FlyInError("nb_drones already defined.")
            case "connection":
                self.settings[setting[0]] = self._parse_metadata(setting[2])
            case "start_hub" | "hub" | "end_hub":
                self.settings[setting[0]] = self._parse_metadata(setting[2])
            case _:
                raise FlyInError(f"'{setting[0]}': Unknown prefix.")

    def _parse_nb_drones(self, line: str) -> None:
        try:
            nb_drones = int(line.strip())
        except ValueError:
            raise FlyInError(f"'{line}': Invalid type for nb_drones.")
        if nb_drones <= 0:
            raise FlyInError(f"'{line}': nb_drones must be a positive "
                             f"values")
        self.nb_drones = nb_drones

    def _parse_zone(self, prefix: str, line: str) -> None:
        setting = line.partition('[')
        params = setting[0].split()
        if len(params) != 3:
            raise FlyInError("Expected 'name x y'.")
        try:
            name, x, y = params[0], int(params[1]), int(params[2])
        except ValueError:
            raise FlyInError("Coordinates must be integers.")
        if "-" in name:
            raise FlyInError("'-': Invalid character for name.")
        if name in self.zones:
            raise FlyInError(f"Duplicate rejected: '{name}' is "
                             f"already defined as a zone.")
        if setting[1] == "[" and setting[2].endswith("]"):
            _parse_metadata(setting[2])


    def _parse_connection:
        ...

    @staticmethod
    def _parse_metadata(line: str) -> dict[str, str]:
        metadata: dict[str, str] = {}
        tags = line.strip().removesuffix("]").split()
        for tag in tags:
            setting = tag.partition("=")
            if not all(setting):
                raise FlyInError(f"'{tag}': Invalid syntax for metadata.")
            if setting[0] in metadata:
                raise FlyInError(f"Duplicate rejected: '{setting[0]}' "
                                 f"already exists in the metadata.")
            metadata[setting[0]] = setting[2]
        return metadata

