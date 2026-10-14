"""Fly-in: route a fleet of drones through a zone network.

Entry point. Reads a map file, computes per-zone distances to the end
zone, and runs the turn-by-turn simulation, either as text output or
in a pygame window (--visual).
"""
import argparse
import sys
from pathlib import Path

from parsing import MapParser
from errors import FlyInError
from pathfinder import PathFinder
from simulation import Simulation
from output import ColorPrinter
from visual import Visualizer

MAX_TURNS = 10000  # safety net (stops a simulation that never finishes)


def parse_args() -> argparse.Namespace:
    """Parse the command-line arguments.

    Returns:
        The parsed arguments: 'map_path' (path to the map file) and
        'visual' (True to open the pygame viewer).
    """
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
    """Run Fly-in on the map given on the command line.

    In text mode, prints one line per turn in the subject's format and
    the total turn count to stderr. In visual mode, opens the viewer.

    Exits with status 1 on an invalid map or an unexpected error,
    printing a one-line message to stderr instead of a traceback.
    """
    try:
        args = parse_args()
        parser = MapParser(args.map_path)

        if args.visual:
            Visualizer(Path(args.map_path)).run()
        else:
            net = parser.read_map()
            distances = PathFinder(net).compute_distances()
            simulation = Simulation(net, distances)
            printer = ColorPrinter()
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
