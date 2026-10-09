from typing import Optional

from drone import Move, ZoneMove, ConnectionMove


RGB = tuple[int, int, int]

COLORS: dict[str, RGB] = {
        "black": (40, 36, 1), "blue": (76, 118, 128), "brown": (104, 63, 46),
        "crimson": (153, 0, 0), "cyan": (0, 255, 255),
        "darkred": (162, 85, 74), "gold": (255, 200, 0),
        "lime": (194, 209, 27), "magenta": (237, 106, 90),
        "maroon": (132, 73, 56), "orange": (246, 153, 45),
        "purple": (150, 0, 205), "red": (212, 99, 85),
        "violet": (84, 22, 180), "yellow": (255, 231, 0),
        "green": (124, 252, 0), "gray": (127, 127, 127),
        }

RAINBOW: list[RGB] = [
        COLORS["red"], COLORS["orange"], COLORS["yellow"],
        COLORS["green"], COLORS["blue"], COLORS["violet"]
        ]

RESET = "\033[0m"


class TextPrinter:
    def format_turn(self, moves: list[Move]) -> str:
        output: list[str] = []
        for move in moves:
            if isinstance(move, ZoneMove):
                output.append(
                        f"D{move.drone.drone_id}-"
                        f"{self._paint(move.zone.name, move.zone.color)}")
            elif isinstance(move, ConnectionMove):
                output.append(
                        f"D{move.drone.drone_id}-{move.connection.name}")
        return " ".join(output)

    def _paint(self, name: str, color: Optional[str]) -> str:
        return name


class ColorPrinter(TextPrinter):
    @staticmethod
    def ansi(rgb: RGB) -> str:
        """Return the terminal escape code for a truecolor foreground."""
        r, g, b = rgb
        return f"\033[38;2;{r};{g};{b}m"

    def _paint(self, name: str, color: Optional[str]) -> str:
        if color == "rainbow":
            rainbow: list[str] = []
            for i, char in enumerate(name):
                rgb = RAINBOW[i % len(RAINBOW)]
                rainbow.append(self.ansi(rgb) + char)
            return "".join(rainbow) + RESET
        elif color is None or color not in COLORS:
            return name
        else:
            return f"{self.ansi(COLORS[color])}{name}{RESET}"
