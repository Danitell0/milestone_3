from enum import Enum
from typing import Optional

from models import Zone, Connection


class DroneState(Enum):
    IN_ZONE = "in_zone"
    IN_FLIGHT = "in_flight"
    DELIVERED = "delivered"


class Drone:
    def __init__(self, drone_id: int, zone: Zone) -> None:
        self.drone_id = drone_id
        self.zone: Optional[Zone] = zone
        self.connection: Optional[Connection] = None
        self.destination: Optional[Zone] = None
        self.state: DroneState = DroneState.IN_ZONE
        self.turns_remaining: int = 0


class Move:
    def __init__(self, drone: Drone) -> None:
        self.drone = drone


class ZoneMove(Move):
    def __init__(self, drone: Drone, zone: Zone) -> None:
        super().__init__(drone)
        self.zone = zone


class ConnectionMove(Move):
    def __init__(self, drone: Drone, connection: Connection) -> None:
        super().__init__(drone)
        self.connection = connection
