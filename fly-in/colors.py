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
