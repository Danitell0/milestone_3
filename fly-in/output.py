from typing import Optional

from drone import Move, ZoneMove, ConnectionMove
from colors import RGB, COLORS, RAINBOW, RESET


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
