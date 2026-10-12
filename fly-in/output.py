"""Printer file to get all moves (colored or uncolored) to readable text."""
from typing import Optional

from drone import Move, ZoneMove, ConnectionMove
from colors import RGB, COLORS, RAINBOW, RESET


class TextPrinter:
    """A plain text printer class for turn output, with no colors."""
    def format_turn(self, moves: list[Move]) -> str:
        """Formats moves to readable text.

        Args:
            moves: A list of moves per each turn.

        Returns:
            The combined list of moves in a str format.
        """
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
        """Prints the name unchanged, subclasses override this with color.

        Args:
            name: Name of the zone.
            color: An optional color so the subclass can color it.

        Returns:
            The unchanged name, subclasses override this to add color.
        """
        return name


class ColorPrinter(TextPrinter):
    """Printer of zone names with their assigned colors."""
    @staticmethod
    def ansi(rgb: RGB) -> str:
        """Return the terminal escape code for a truecolor foreground.

        Args:
            rgb: tuple of rgb values.

        Returns:
            Ansi code to be added before the str.
        """
        r, g, b = rgb
        return f"\033[38;2;{r};{g};{b}m"

    def _paint(self, name: str, color: Optional[str]) -> str:
        """Colorizes the name with the optional color.

        Checking for the name of each zone to assign their case. If 'rainbow'
        every character of the name will have different color, if None or an
        unknown color it will return the unchanged name or else it will use
        the 'color' to print the name colored with ansi code.

        Args:
            name: Name of the zone.
            color: An optional color to add to the characters.

        Returns:
            Either the unchanged name or the colorized name of the zone.
        """
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
