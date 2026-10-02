"""Class for each zone of the simulation

With each role and type in smaller Enum classes.
"""

from enum import Enum
from typing import Optional


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
        max_drones: Max number of drones allowed in the zone simoultanious,
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
