from errors import FlyInError
from drone import Drone, DroneState, Move, ZoneMove, ConnectionMove
from models import Map, Zone, ZoneRole, ZoneType, Connection


class Simulation:
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
        return moves

    def _turns_left(self, drone: Drone) -> int:
        if drone.state == DroneState.IN_ZONE:
            if drone.zone is not None:
                return self.distances[drone.zone.name]
        if drone.destination is not None:
            return (self.distances[drone.destination.name] +
                    drone.turns_remaining)
        raise FlyInError(f"{drone.drone_id}: "
                         f"inconsistent state {drone.state}.")

    def is_finished(self) -> bool:
        return not self.active_drones

    def _count_occupancy(self) -> None:
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
        if zone.zone_role in (ZoneRole.START, ZoneRole.END):
            return True
        return self.zone_load.get(zone.name, 0) < zone.max_drones

    def _link_has_room(self, connection: Connection) -> bool:
        return (self.link_load.get(connection.key, 0) <
                connection.max_link_capacity)

    def _ranked_options(self,
                        drone: Drone) -> list[tuple[int, Zone, Connection]]:

        candidates: list[tuple[int, Zone, Connection]] = []

        if drone.zone is None:
            raise FlyInError(f"{drone.drone_id}: has no zone.")
        for zone, connection in self.network.neighbours[drone.zone.name]:
            if zone.name not in self.distances:
                continue
            score = zone.cost + self.distances[zone.name]
            candidates.append((score, zone, connection))

            candidates.sort(key=lambda item: item[0])
        return candidates

    def _move_drone(self, drone: Drone,
                    new_zone: Zone,
                    connection: Connection) -> Move:
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

