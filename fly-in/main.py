import argparse
import sys

from parsing import MapParser
from errors import FlyInError
from pathfinder import PathFinder
from simulation import Simulation
from output import ColorPrinter
from visual import Visualizer

MAX_TURNS = 10000


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
        simulation = Simulation(net, distances)
        printer = ColorPrinter()

        # debug section

        if args.visual:
            Visualizer(net).run()
            return

        # end debug section

        while not simulation.is_finished():
            if simulation.turn >= MAX_TURNS:
                raise FlyInError("Simulation did not finish.")
            moves = simulation.step()
            print(printer.format_turn(moves))
        print(f"Simulation finished in {simulation.turn} turns.",
              file=sys.stderr)
    except FlyInError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Internal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
