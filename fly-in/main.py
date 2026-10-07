import argparse

from parsing import MapParser
from errors import FlyInError

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
        print(net.nb_drones)
        print(net.start.name, net.end.name)
    except FlyInError as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
