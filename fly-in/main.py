import argparse

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
    args = parse_args()
    print("Hello World!")

if __name__ == "__main__":
    main()
