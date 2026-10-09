import heapq

from errors import FlyInError
from models import Map, ZoneType


class PathFinder:
    def __init__(self, network: Map) -> None:
        self.network = network

    def compute_distances(self) -> dict[str, int]:
        heap: list[tuple[int, str]] = [(0, self.network.end.name)]
        distances: dict[str, int] = {self.network.end.name: 0}

        while heap:
            dist, name = heapq.heappop(heap)
            if dist > distances[name]:
                continue
            for neighbour in self.network.neighbours[name]:
                n_zone, _ = neighbour
                if n_zone.zone_type == ZoneType.BLOCKED:
                    continue
                new_distance = dist + self.network.zones[name].cost
                if (n_zone.name not in distances
                        or new_distance < distances[n_zone.name]):
                    distances[n_zone.name] = new_distance
                    heapq.heappush(heap, (new_distance, n_zone.name))

        if self.network.start.name not in distances:
            raise FlyInError("Starting point is unreachable.")

        return distances
