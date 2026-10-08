import argparse

from parsing import MapParser
from errors import FlyInError
from pathfinder import PathFinder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description=("Route a fleet of drones from start to end through a"
                         " zone network.")
            )
    parser.add_argument("map_path")
    parser.add_argument("--visual",
                        action="store_true",
                        help="Run the program with visual mode.")

    args = parser.parse_args()

    return args


def main() -> None:
    try:
        args = parse_args()
        parser = MapParser(args.map_path)
        net = parser.read_map()
        distances = PathFinder(net).compute_distances()
        for zone_name, turns in sorted(distances.items(), key=lambda item: item[1]):
            print(f"{zone_name:>20} : {turns}")
    except FlyInError as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
