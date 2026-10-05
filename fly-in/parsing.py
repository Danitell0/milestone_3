from pathlib import Path
from typing import Optional

from .errors import FlyInError
from .network import Map

class MapParser:
    def __init__(self, map_path: Path) -> None:
        self.map_path = map_path
        self.settings = {}

        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}

        self.is_start = False
        self.is_end = False

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

        zone_role = ZoneRole(prefix)
        if zone_role == ZoneRole.START:
            if self.is_start:
                raise FlyInError("Starting point was already defined.")
            self.is_start = True
        elif zone_role == ZoneRole.END:
            if self.is_end:
                raise FlyInError("Ending point was already defined.")
            self.is_end = True


        metadata: dict[str, str] = {}
        zone_type = ZoneType.NORMAL
        max_drones = 1
        color: Optional[str] = None

        if setting[1] == "[":
            if not setting[2].strip().endswith(']'):
                raise FlyInError(f"'{setting[2]}': Invalid syntax.")
            allowed_fields = {'zone', 'color', 'max_drones'}
            metadata = self._parse_metadata(setting[2])
            if not metadata.keys() <= allowed_fields:
                raise FlyInError(f"'{metadata.keys() - allowed_fields}': "
                                 f"Invalid tag in metadata.")
            try:
                if "zone" in metadata:
                    zone_type = ZoneType(metadata["zone"])
            except ValueError:
                raise FlyInError(f"'{metadata['zone']}': "
                                 f"Unknown type of zone.")
            try:
                if zone_role == ZoneRole.HUB:
                    if "max_drones" in metadata:
                        max_drones = int(metadata["max_drones"])
            except ValueError:
                raise FlyInError("max_drones must be an integer.")
            if max_drones <= 0:
                raise FlyInError("max_drones must be greater than 0.")
            if "color" in metadata:
                color = metadata["color"]

        self.zones[name] = Zone(name, 
                                x, y,
                                zone_role,
                                zone_type,
                                color,
                                max_drones)


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

