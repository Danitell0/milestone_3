"""Zones, connections and the map that links them."""
from enum import Enum
from typing import Optional

from errors import FlyInError


class ZoneType(Enum):
    """The kind of zone, which decides how drones can use it.

    Attributes:
        NORMAL: Takes 1 turn to enter.
        BLOCKED: Drones cannot enter it.
        PRIORITY: Takes 1 turn to enter.
        RESTRICTED: Takes 2 turns to enter.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    PRIORITY = "priority"
    RESTRICTED = "restricted"


class ZoneRole(Enum):
    """The role a zone plays in the map.

    Attributes:
        START: Zone where all drones begin.
        END: Zone all drones must reach.
        HUB: Any zone in between.
    """
    START = "start_hub"
    END = "end_hub"
    HUB = "hub"


class Zone:
    """A place on the map where drones can stop.

    Attributes:
        name: Unique name of the zone.
        x: Horizontal position on the map.
        y: Vertical position on the map.
        zone_role: Role of the zone in the map.
        zone_type: Kind of zone (Defaults to NORMAL).
        color: Color name used when drawing the zone (or None).
        max_drones: Max drones allowed in the zone at once (Defaults to 1).
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
        """Turns needed to move into this zone."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1


class Connection:
    """A link between two zones that drones can fly along.

    Attributes:
        zone_a: First zone of the connection.
        zone_b: Second zone of the connection.
        max_link_capacity: Max drones on the connection at once
            (Defaults to 1).
    """
    def __init__(self, zone_a: Zone, zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    @property
    def key(self) -> tuple[str, str]:
        """Sorted pair of zone names, so A-B and B-A give the same key."""
        return (min(self.zone_a.name, self.zone_b.name),
                max(self.zone_a.name, self.zone_b.name))

    @property
    def name(self) -> str:
        """Name used in the output (ex: roof-corridor)."""
        return f"{self.zone_a.name}-{self.zone_b.name}"


class Map:
    """The full network of zones and connections for a simulation

    Attributes:
        nb_drones: Number of drones in the simulation.
        zones: Zones keyed by name.
        connections: Connections keyed by their sorted pair of zone names.
        start: Zone where the drones begin.
        end: Zone the drones must reach.
        neighbours: Zone names mapped to a list of pairs.
    """
    def __init__(self, nb_drones: int,
                 zones: dict[str, Zone],
                 connections: dict[tuple[str, str], Connection]) -> None:
        """Set up the map and find its start and end zones.

        Raises:
            FlyInError: If the map has no start or no end zone.
        """
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
