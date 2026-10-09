"""Class for each zone of the simulation

With each role and type in smaller Enum classes.
"""

from enum import Enum
from typing import Optional

from errors import FlyInError


class ZoneType(Enum):
    """Parameter types for type for each zone.

    A NORMAL and a PRIORITY zone will both take 1 turn to move to,
    a RESTRICTED zone will take an 'n' amount of turns to move to,
    a BLOCKED zone will be unavailable for the drones to land.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    PRIORITY = "priority"
    RESTRICTED = "restricted"


class ZoneRole(Enum):
    """Parameter types for defining each zone role.

    START will define the zone where all the drones will start the simulation,
    END will define the goal zone where all the drones should finish, and
    HUB defines all the zones in between them.
    """
    START = "start_hub"
    END = "end_hub"
    HUB = "hub"


class Zone:
    """Builds each zone with all the necessary information for the simulation.

    Attributes:
        name: custom name for the zone.
        x: coordinate for horizontal in int format.
        y: coordinate for vertical in int format.
        zone_role: role for the zone (start, end or hub).
        zone_type: type of the zone (normal, blocked, priority or restricted),
            if not defined it will be defaulted to NORMAL.
        color: an optional parameter to define the color of the zone.
        max_drones: Max number of drones allowed in the zone simultaneously,
            if not defined it will be defaulted to 1.
    """
    def __init__(self, name: str, x: int, y: int,
                 role: ZoneRole, zone_type: ZoneType = ZoneType.NORMAL,
                 color: Optional[str] = None, max_drones: int = 1) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_role = role
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

    @property
    def cost(self) -> int:
        """Cost of moving INTO this zone, in turns."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1


class Connection:
    """Build a connection between two Zones.

    Attributes:
        zone_a: first zone of the connection.
        zone_b: second zone of the connection.
        max_link_capacity: number of drones allowed to traverse this
            connection simultaneously.
    """
    def __init__(self, zone_a: Zone, zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    @property
    def key(self) -> tuple[str, str]:
        return (min(self.zone_a.name, self.zone_b.name),
                max(self.zone_a.name, self.zone_b.name))

    @property
    def name(self) -> str:
        return f"{self.zone_a.name}-{self.zone_b.name}"


class Map:
    """Build a network of zones and connections.

    Attributes:
        nb_drones: number of drones in the simulation.
        zones: dictionary of zones in the map with the name as a key.
        connections: dictionary of connections in the map with the zones
            keyed by the alphabetically ordered pair of zone names.
        start: starting zone of the map.
        end: ending zone of the map.
        neighbours: a dictionary to connect the zone to its neighbour zones.
    """
    def __init__(self, nb_drones: int,
                 zones: dict[str, Zone],
                 connections: dict[tuple[str, str], Connection]) -> None:
        self.nb_drones = nb_drones
        self.zones = zones
        self.connections = connections

        start: Optional[Zone] = None
        end: Optional[Zone] = None
        for zone in self.zones.values():
            if zone.zone_role == ZoneRole.START:
                start = zone
            elif zone.zone_role == ZoneRole.END:
                end = zone

        if start is None:
            raise FlyInError("Impossible to generate Map with no "
                             "starting point.")
        self.start = start
        if end is None:
            raise FlyInError("Impossible to generate Map with no "
                             "ending point.")
        self.end = end

        self._build_neighbours()

    def _build_neighbours(self) -> None:
        """Connect each zone to its neighbours."""
        neighbours: dict[str, list[tuple[Zone, Connection]]] = {
                name: [] for name in self.zones
                }

        for connection in self.connections.values():
            neighbours[connection.zone_a.name].append((
                    connection.zone_b, connection))
            neighbours[connection.zone_b.name].append((
                    connection.zone_a, connection))

        self.neighbours = neighbours
