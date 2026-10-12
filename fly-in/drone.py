"""Drones, their state and the moves they make each turn."""
from enum import Enum
from typing import Optional

from models import Zone, Connection


class DroneState(Enum):
    """Where a drone is during the simulation.

    Attributes:
        IN_ZONE: Parked in a zone, ready to move.
        IN_FLIGHT: On a connection, heading to a restricted zone.
        DELIVERED: Reached the end zone and no longer moves.
    """
    IN_ZONE = "in_zone"
    IN_FLIGHT = "in_flight"
    DELIVERED = "delivered"


class Drone:
    """A drone travelling from the start zone to the end zone.

    Attributes:
        drone_id: Number shown in the output (ex: D1).
        zone: Zone the drone is in or None while in flight.
        connection: Connection being flown or None while in a zone.
        destination: Zone being flown to or None while in a zone.
        state: Current state of the drone.
        turns_remaining: Turns left before landing at the destination.
    """
    def __init__(self, drone_id: int, zone: Zone) -> None:
        self.drone_id = drone_id
        self.zone: Optional[Zone] = zone
        self.connection: Optional[Connection] = None
        self.destination: Optional[Zone] = None
        self.state: DroneState = DroneState.IN_ZONE
        self.turns_remaining: int = 0


class Move:
    """The base class for one drone's action in a single turn.

    Attributes:
        drone: The drone making the move
    """
    def __init__(self, drone: Drone) -> None:
        self.drone = drone


class ZoneMove(Move):
    """The drone lands in a zone and gets printed (D1-roof).

    Attributes:
        zone: The zone where the drone is landing.
    """
    def __init__(self, drone: Drone, zone: Zone) -> None:
        super().__init__(drone)
        self.zone = zone


class ConnectionMove(Move):
    """The drone is in flight on a connection printed as (D1-roof-corridor)

    Attributes:
        connection: The connection flight where the drone is flying.
    """
    def __init__(self, drone: Drone, connection: Connection) -> None:
        super().__init__(drone)
        self.connection = connection
