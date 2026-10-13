"""Turn-by-turn simulation of the drones flying from start to end."""
from errors import FlyInError
from drone import Drone, DroneState, Move, ZoneMove, ConnectionMove
from models import Map, Zone, ZoneRole, ZoneType, Connection


class Simulation:
    """Moves every drone one turn at a time untill all are delivered.

    Attributes:
        network: The map the drones fly on.
        distances: Zone names mapped to their distance in turns from the end.
        zone_load: Zone names mapped to the number of drones in or flying
            to them.
        link_load: Connection keys mapped to the number of drones on them.
        active_drones: Drones that haven't been delivered yet.
        turn: Number of turns played so far.
    """
    def __init__(self, network: Map, distances: dict[str, int]) -> None:
        self.network = network
        self.distances = distances
        self.zone_load: dict[str, int] = {}
        self.link_load: dict[tuple[str, str], int] = {}

        # creating Drones by ID and setting them in START
        self.active_drones: list[Drone] = [
                Drone(i, self.network.start)
                for i in range(1, self.network.nb_drones + 1)]
        self.turn = 0

    def step(self) -> list[Move]:
        """Play one turn of the simulation.

        Drones closest to the end move first. Drones in flight get one turn
        closer to landing. Drones in a zone take their best option if it has
        room, otherwise they wait. Drones that reached the end zone are
        delivered and removed from the active drones.

        Returns:
            Every move made this turn.

        Raises:
            FlyInError: If a drone in flight has no destination.
        """
        moves: list[Move] = []
        self._count_occupancy()
        self.active_drones.sort(
                key=lambda drone: (self._turns_left(drone), drone.drone_id))

        for drone in self.active_drones:
            if drone.state == DroneState.IN_FLIGHT:
                drone.turns_remaining -= 1
                landing_zone = drone.destination
                if landing_zone is None:
                    raise FlyInError(
                            f"{drone.drone_id} missing destination zone")

                if drone.turns_remaining == 0:
                    drone.zone = landing_zone
                    drone.state = DroneState.IN_ZONE
                    moves.append(ZoneMove(drone, landing_zone))
                    if drone.connection is not None:
                        link_key = drone.connection.key
                        self.link_load[link_key] -= 1
                    drone.connection = None
                    drone.destination = None
                continue
            # if drone.state == IN_ZONE
            candidates = self._ranked_options(drone)
            if not candidates:
                continue
            best_score, _, _ = candidates[0]
            for score, new_zone, connection in candidates:
                if not (self._zone_has_room(new_zone) and
                        self._link_has_room(connection)):
                    continue
                elif score < best_score + 1:
                    moves.append(
                            self._move_drone(drone, new_zone, connection))
                break

        # deliver drones to END
        for drone in self.active_drones:
            if drone.zone is self.network.end:
                drone.state = DroneState.DELIVERED
        self.active_drones = [drone for drone in self.active_drones if
                              drone.zone is not self.network.end]

        self.turn += 1
        self._check_capacity()
        return moves

    def _turns_left(self, drone: Drone) -> int:
        """Estimate how many turns a drone needs to reach the end.

        Args:
            drone: The drone to check.

        Returns:
            Distance from its zone or from its destination plus the turns
            left in flight.

        Raises:
            FlyInError: If the drone has neither a zone nor a destination.
        """
        if drone.state == DroneState.IN_ZONE:
            if drone.zone is not None:
                return self.distances[drone.zone.name]
        if drone.destination is not None:
            return (self.distances[drone.destination.name] +
                    drone.turns_remaining)
        raise FlyInError(f"{drone.drone_id}: "
                         f"inconsistent state {drone.state}.")

    def is_finished(self) -> bool:
        """Return whether every drone has been delivered."""
        return not self.active_drones

    def _count_occupancy(self) -> None:
        """Recount how many drones are in each zone and connection.

        Drones in flight count towards both their connection and their
        destination zone.
        """
        self.zone_load = {}
        self.link_load = {}

        for drone in self.active_drones:
            if drone.state == DroneState.IN_ZONE:
                if drone.zone is not None:
                    name = drone.zone.name
                    self.zone_load[name] = self.zone_load.get(name, 0) + 1
            elif drone.state == DroneState.IN_FLIGHT:
                if (drone.destination is not None and
                        drone.connection is not None):
                    dest = drone.destination.name
                    link_key = drone.connection.key
                    self.zone_load[dest] = self.zone_load.get(dest, 0) + 1
                    self.link_load[
                        link_key] = self.link_load.get(link_key, 0) + 1

    def _zone_has_room(self, zone: Zone) -> bool:
        """Check if a drone can move into a zone.

        Start and end zones have no limit.

        Args:
            zone: The zone to check.

        Returns:
            True if the zone is below its max_drones.
        """
        if zone.zone_role in (ZoneRole.START, ZoneRole.END):
            return True
        return self.zone_load.get(zone.name, 0) < zone.max_drones

    def _link_has_room(self, connection: Connection) -> bool:
        """Check if a drone can fly on a connection.

        Args:
            connection: The connection to check.

        Returns:
            True if the connection is below its max_link_capacity.
        """
        return (self.link_load.get(connection.key, 0) <
                connection.max_link_capacity)

    def _ranked_options(self,
                        drone: Drone) -> list[tuple[int, Zone, Connection]]:
        """List the zones a drone can move to, best option first.

        Each option is scored by the cost of entering the zone plus its
        distance to the end. Ties go to priority zones. Unreachable zones
        are left out.

        Args:
            drone: The drone choosing where to move.

        Returns:
            (score, zone, connection) tuples sorted by score.

        Raises:
            FlyInError: If the drone is not in a zone.
        """
        candidates: list[tuple[int, Zone, Connection]] = []

        if drone.zone is None:
            raise FlyInError(f"{drone.drone_id}: has no zone.")
        for zone, connection in self.network.neighbours[drone.zone.name]:
            if zone.name not in self.distances:
                continue
            score = zone.cost + self.distances[zone.name]
            candidates.append((score, zone, connection))

        candidates.sort(key=lambda item: (item[0], item[1].zone_type !=
                                          ZoneType.PRIORITY))
        return candidates

    def _move_drone(self, drone: Drone,
                    new_zone: Zone,
                    connection: Connection) -> Move:
        """Move a drone towards a new zone and update the loads.

        Moving into a resticted zone puts the drone in flight on the
        connection until it lands.

        Args:
            drone: The drone to move.
            new_zone: The zone it moves to.
            connection: The connection it uses.

        Returns:
            A ConnectionMove if the drone is now in flight, otherwise
            a ZoneMove.

        Raises:
            FlyInError: If the drone is not in a zone.
        """
        old_zone = drone.zone
        if old_zone is None:
            raise FlyInError(f"{drone.drone_id} missing current zone")
        self.zone_load[old_zone.name] -= 1
        self.zone_load[new_zone.name] = self.zone_load.get(new_zone.name,
                                                           0) + 1
        link_key = connection.key
        self.link_load[link_key] = self.link_load.get(link_key, 0) + 1
        if new_zone.zone_type == ZoneType.RESTRICTED:
            drone.state = DroneState.IN_FLIGHT
            drone.zone = None
            drone.connection = connection
            drone.destination = new_zone
            drone.turns_remaining = new_zone.cost - 1
            return ConnectionMove(drone, connection)
        else:
            drone.zone = new_zone
            return ZoneMove(drone, new_zone)

    def _check_capacity(self) -> None:
        """Make sure no zone or connection is over the limit.

        This is a safety check: If it fails, the simulation itself has a bug.

        Raises:
            RuntimeError: If a zone or connection holds too many drones.
        """
        for zone, load in self.zone_load.items():
            curr_zone = self.network.zones[zone]

            if curr_zone.zone_role in (ZoneRole.START, ZoneRole.END):
                continue
            if load > curr_zone.max_drones:
                raise RuntimeError(
                        f"Number of drones in {curr_zone.name} "
                        f"passes its own limit on turn {self.turn}.")
        for link, load in self.link_load.items():
            curr_connection = self.network.connections[link]

            if load > curr_connection.max_link_capacity:
                raise RuntimeError(
                        f"Number of drones in {curr_connection.name}"
                        f" passes its own limit on turn {self.turn}.")
