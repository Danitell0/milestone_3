from dataclasses import dataclass
from enum import Enum, auto

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

DEFAULT_ZONE_COLOR = (220, 220, 220)

RAINBOW: list[RGB] = [
        COLORS["red"], COLORS["orange"], COLORS["yellow"],
        COLORS["green"], COLORS["blue"], COLORS["violet"]
        ]

RESET = "\033[0m"


class Texture(Enum):
    NONE = auto()
    GRID = auto()
    DOTS = auto()
    SCANLINES = auto()
    RINGS = auto()
    COLUMNS = auto()


@dataclass(frozen=True)
class Theme:
    name: str
    background: RGB
    trace: RGB
    pad_ring: RGB
    silkscreen: RGB
    hud_bg: RGB
    hud_text: RGB
    drone_led: RGB
    texture: Texture = Texture.NONE
    texture_color: RGB = (0, 0, 0)


BLUEPRINT = Theme(name="Blueprint",
                  background=(24, 56, 102),
                  trace=(170, 200, 235),
                  pad_ring=(235, 242, 250),
                  silkscreen=(235, 242, 250),
                  hud_bg=(14, 34, 64),
                  hud_text=(200, 222, 245),
                  drone_led=(255, 196, 70),
                  texture=Texture.GRID,
                  texture_color=(40, 78, 130))

RADAR = Theme(name="Radar",
              background=(8, 18, 14),
              trace=(40, 110, 70),
              pad_ring=(90, 200, 130),
              silkscreen=(140, 230, 170),
              hud_bg=(16, 32, 24),
              hud_text=(120, 255, 160),
              drone_led=(255, 220, 90),
              texture=Texture.RINGS,
              texture_color=(18, 44, 30))

PAPER = Theme(name="Paper",
              background=(244, 238, 222),
              trace=(150, 140, 125),
              pad_ring=(60, 55, 50),
              silkscreen=(50, 46, 42),
              hud_bg=(226, 218, 198),
              hud_text=(50, 46, 42),
              drone_led=(214, 72, 60),
              texture=Texture.DOTS,
              texture_color=(222, 214, 194))

MATRIX = Theme(name="Matrix",
               background=(2, 10, 4),
               trace=(0, 90, 30),
               pad_ring=(0, 200, 70),
               silkscreen=(120, 255, 140),
               hud_bg=(4, 24, 10),
               hud_text=(0, 255, 65),
               drone_led=(200, 255, 200),
               texture=Texture.COLUMNS,
               texture_color=(14, 44, 22))

AMBER = Theme(name="Amber",
              background=(18, 12, 4),
              trace=(120, 72, 10),
              pad_ring=(255, 176, 0),
              silkscreen=(255, 204, 102),
              hud_bg=(36, 24, 6),
              hud_text=(255, 176, 0),
              drone_led=(255, 240, 200),
              texture=Texture.SCANLINES,
              texture_color=(52, 36, 12))

OCEAN = Theme(name="Ocean",
              background=(10, 36, 48),
              trace=(30, 110, 120),
              pad_ring=(110, 210, 200),
              silkscreen=(220, 245, 245),
              hud_bg=(6, 24, 34),
              hud_text=(130, 230, 220),
              drone_led=(255, 127, 102),
              texture=Texture.DOTS,
              texture_color=(18, 54, 70))

SAKURA = Theme(name="Sakura",
               background=(250, 232, 236),
               trace=(222, 170, 186),
               pad_ring=(160, 90, 120),
               silkscreen=(90, 50, 70),
               hud_bg=(238, 206, 216),
               hud_text=(90, 50, 70),
               drone_led=(120, 170, 120),
               texture=Texture.DOTS,
               texture_color=(240, 214, 222))

THEMES: list[Theme] = [BLUEPRINT, RADAR, PAPER, MATRIX, AMBER, OCEAN, SAKURA]
