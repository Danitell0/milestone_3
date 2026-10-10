import pygame
import math
import random

from pathlib import Path
from typing import Optional
from simulation import Simulation
from models import Map, Zone
from colors import Texture, THEMES, COLORS, DEFAULT_ZONE_COLOR, RGB, RAINBOW
from parsing import MapParser
from pathfinder import PathFinder
from simulation import Simulation
from errors import FlyInError

# animation
TURN_DELAY = 600
SPEEDS = [1, 2, 4]
CONTROLS = ["[Space]: play / pause", "[->]: next turn",
            "[F]: fast forward", "[T]: change theme",
            "[R]: reset simulation"
            "[Q]: quit program",]
GLOW_RADIUS = 35
BUMP_TIME = 250
BUMP_SIZE = 6

# window
WIDTH = 1800
HEIGHT = 1000
GRID_STEP = 40
DOT_STEP = 30
SCAN_STEP = 6
COLUMN_STEP = 10
RING_STEP = 120
MARGIN = 80

# zone
RADIUS = 20


class Visualizer:
    def __init__(self, path: Path) -> None:
        pygame.init()

        self.map_path = path

        # --------- Visual Control
        self.speed_index: int = 0
        self.theme_index: int = 0
        self.last_step: int = 0
        self.error: Optional[str] = None

        # ---------- Animation
        self.from_pos: dict[int, tuple[int, int]] = {}
        self.to_pos: dict[int, tuple[int, int]] = {}
        self.anim_start: int = 0
        self.bump_start: dict[str, int] = {}

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        # text fonts
        self.font = pygame.font.Font(None, 13)
        self.nb_font = pygame.font.Font(None, 20)
        self.counter_font = pygame.font.Font(None, 70)
        self.control_font = pygame.font.Font(None, 50)

        self._load_map(path)
        self._reset_view()
        self._apply_theme()
        pygame.display.set_caption("Fly-in project by danmorei")

    def _load_map(self, path: Path) -> None:
        try:
            network = MapParser(path).read_map()
            distances = PathFinder(network).compute_distances()
            sim = Simulation(network, distances)
        except FlyInError as e:
            self.error = str(e)
            return
        self.network = network
        self.sim = sim
        self.map_path = path
        self.error = None
        self._reset_view()

    def _reset_view(self) -> None:
        self.paused: bool = True

        # ---------- Map scale compute
        self.min_x = min(zone.x for zone in self.network.zones.values())
        self.max_x = max(zone.x for zone in self.network.zones.values())
        self.min_y = min(zone.y for zone in self.network.zones.values())
        self.max_y = max(zone.y for zone in self.network.zones.values())
        self.usable_w = WIDTH - 2 * MARGIN
        self.usable_h = HEIGHT - 2 * MARGIN

        # max() in case of 0
        self.range_x = max((self.max_x - self.min_x), 1)
        self.range_y = max((self.max_y - self.min_y), 1)
        self.scale = min((self.usable_w / self.range_x),
                         (self.usable_h / self.range_y))

        self.from_pos = self._drone_positions()
        self.to_pos = self.from_pos

        # reseting map
        self.anim_start: int = 0
        self.last_step: int = 0
        self.bump_start: dict[str, int] = {}

    def run(self) -> None:
        running = True
        while running:
            # control block
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.paused:
                        if not self.sim.is_finished():
                            self._do_step()
                            self.last_step = pygame.time.get_ticks()
                    elif event.key == pygame.K_SPACE:
                        if not self.sim.is_finished():
                            self.paused = not self.paused
                    elif event.key == pygame.K_f:
                        self.speed_index = (
                                self.speed_index + 1) % len(SPEEDS)
                    elif event.key == pygame.K_t:
                        self.theme_index = (
                                self.theme_index + 1) % len(THEMES)
                        self._apply_theme()
                    elif event.key == pygame.K_r:
                        self._load_map(self.map_path)
                        self._reset_view()
                    elif event.key == pygame.K_q:
                        running = False

            # time block
            now = pygame.time.get_ticks()
            if (not self.paused
                    and not self.sim.is_finished()
                    and now - self.last_step >= (TURN_DELAY //
                                                 SPEEDS[self.speed_index])):
                self._do_step()
                self.last_step = now

            # drawing block
            self.screen.blit(self.background, (0, 0))
            self._draw_hud()
            if self.sim.is_finished():
                turn_text = f"Finished in {self.sim.turn} turns"
            else:
                turn_text = f"Turn {self.sim.turn}"
            display_text = self.counter_font.render(turn_text,
                                                    True,
                                                    self.theme.silkscreen)
            self.screen.blit(display_text, (20, 20))
            self._draw_map()
            self._draw_drones()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def _to_pixel(self, zone: Zone) -> tuple[int, int]:
        px = MARGIN + (zone.x - self.min_x) * self.scale
        py = MARGIN + (zone.y - self.min_y) * self.scale
        return (int(px), int(py))

    def _draw_map(self) -> None:
        now = pygame.time.get_ticks()
        # drawing the links
        for link in self.network.connections.values():
            pygame.draw.line(
                    self.screen,
                    self.theme.trace,
                    self._to_pixel(link.zone_a),
                    self._to_pixel(link.zone_b),
                    5)

        # drawing the zones
        for zone in self.network.zones.values():
            px, py = self._to_pixel(zone)
            pygame.draw.circle(
                    self.screen,
                    self.theme.pad_ring,
                    (px, py),
                    (self._zone_radius(zone.name, now) + 3))
            pygame.draw.circle(
                    self.screen,
                    self._zone_rgb(zone),
                    (px, py),
                    self._zone_radius(zone.name, now))
            text = self.font.render(zone.name, True, self.theme.silkscreen)
            rect = text.get_rect(
                    center=(px, py + RADIUS + 10))
            self.screen.blit(text, rect)

    def _zone_counts(self) -> dict[str, int]:
        counter: dict[str, int] = {}
        for drone in self.sim.active_drones:
            if drone.zone is None:
                continue
            counter[drone.zone.name] = counter.get(drone.zone.name, 0) + 1
        return counter

    def _zone_radius(self, name: str, now: int) -> int:
        start = self.bump_start.get(name)
        if start is None:
            return RADIUS
        elapsed = now - start
        if 0 <= elapsed < BUMP_TIME:
            return RADIUS + int(BUMP_SIZE * (1 - elapsed / BUMP_TIME))
        else:
            return RADIUS

    def _draw_drones(self) -> None:
        counts: dict[str, int] = {}

        # gliding block
        now = pygame.time.get_ticks()
        t = min(1.0, (now - self.anim_start) / self._glide_duration())

        for drone in self.sim.active_drones:
            if drone.zone is None:
                continue
            counts[drone.zone.name] = counts.get(drone.zone.name, 0) + 1
        for drone_id, end in self.to_pos.items():
            start = self.from_pos.get(drone_id, end)
            if start == end or t >= 1.0:
                continue
            x, y = self._glide_between(start, end, t)
            self.screen.blit(self.glow, (x - GLOW_RADIUS, y - GLOW_RADIUS))
            pygame.draw.circle(self.screen, self.theme.drone_led, (x, y), 6)
        for name, count in counts.items():
            zone = self.sim.network.zones[name]
            px, py = self._to_pixel(zone)
            text = self.nb_font.render(
                    f"{count}", True, self.theme.silkscreen)
            rect = text.get_rect(center=(px, py))
            self.screen.blit(text, rect)

    def _drone_positions(self) -> dict[int, tuple[int, int]]:
        positions: dict[int, tuple[int, int]] = {}
        for drone in self.sim.active_drones:
            if drone.zone is None and drone.connection:
                x1, y1 = self._to_pixel(drone.connection.zone_a)
                x2, y2 = self._to_pixel(drone.connection.zone_b)
                midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
                positions[drone.drone_id] = midpoint
            elif drone.zone is None:
                continue
            else:
                positions[drone.drone_id] = self._to_pixel(drone.zone)
        return positions

    def _glide_duration(self) -> float:
        duration = (TURN_DELAY // SPEEDS[self.speed_index]) * 0.8
        return duration

    def _do_step(self) -> None:
        self.from_pos = self._drone_positions()
        before = self._zone_counts()
        self.sim.step()
        self.to_pos = self._drone_positions()
        after = self._zone_counts()
        self.anim_start = pygame.time.get_ticks()
        for drone_id in self.from_pos:
            if drone_id not in self.to_pos:
                self.to_pos[drone_id] = self._to_pixel(self.network.end)
        for name in set(before) | set(after):
            if before.get(name, 0) < after.get(name, 0):
                self.bump_start[
                        name] = self.anim_start + int(self._glide_duration())
            else:
                self.bump_start[name] = self.anim_start

    @staticmethod
    def _glide_between(a: tuple[int, int],
                       b: tuple[int, int],
                       t: float) -> tuple[int, int]:
        ax, ay = a
        bx, by = b
        axis_a = ax + (bx - ax) * t
        axis_b = ay + (by - ay) * t
        return (int(axis_a), int(axis_b))

    def _draw_hud(self) -> None:
        # position
        line_height = self.control_font.get_linesize()
        start_y = HEIGHT - 20 - len(CONTROLS) * line_height

        rendered: list[pygame.Surface] = []
        for command in CONTROLS:
            rendered.append(self.control_font.render(command,
                                                     True,
                                                     self.theme.hud_text))
        # box
        pad = 10
        width = max(t.get_width() for t in rendered) + (pad * 2)
        height = len(CONTROLS) * line_height + (pad * 2)
        box_y = start_y - pad
        box_x = 20 - pad
        pygame.draw.rect(self.screen,
                         self.theme.hud_bg,
                         (box_x, box_y, width, height),
                         border_radius=8)
        for i, text in enumerate(rendered):
            y = start_y + i * line_height
            self.screen.blit(text, (20, y))

    def _zone_rgb(self, zone: Zone) -> RGB:
        if zone.color == "rainbow":
            return RAINBOW[(pygame.time.get_ticks() // 300) % len(RAINBOW)]
        return COLORS.get(zone.color or "", DEFAULT_ZONE_COLOR)

    def _build_glow(self) -> pygame.Surface:
        glow = pygame.Surface((GLOW_RADIUS * 2, GLOW_RADIUS * 2),
                              pygame.SRCALPHA)
        r, g, b = self.theme.drone_led
        layers = [(GLOW_RADIUS, 25), (GLOW_RADIUS * 2 // 3, 60),
                  (GLOW_RADIUS // 3, 110)]
        center = (GLOW_RADIUS, GLOW_RADIUS)

        for size, alpha in layers:
            pygame.draw.circle(glow, (r, g, b, alpha), center, size)
        return glow

    def _build_background(self) -> pygame.Surface:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(self.theme.background)
        match self.theme.texture:
            case Texture.GRID:
                for x in range(0, WIDTH, GRID_STEP):
                    pygame.draw.line(bg, self.theme.texture_color,
                                     (x, 0), (x, HEIGHT))
                for y in range(0, HEIGHT, GRID_STEP):
                    pygame.draw.line(bg, self.theme.texture_color,
                                     (0, y), (WIDTH, y))
            case Texture.DOTS:
                for x in range(0, WIDTH, DOT_STEP):
                    for y in range(0, HEIGHT, DOT_STEP):
                        pygame.draw.circle(bg, self.theme.texture_color,
                                           (x, y), 2)
            case Texture.SCANLINES:
                for y in range(0, HEIGHT, SCAN_STEP):
                    pygame.draw.line(bg, self.theme.texture_color,
                                     (0, y), (WIDTH, y), width=2)
            case Texture.RINGS:
                center = (WIDTH // 2, HEIGHT // 2)
                max_radius = int(math.hypot(WIDTH // 2, HEIGHT // 2))
                for r in range(RING_STEP, max_radius, RING_STEP):
                    pygame.draw.circle(bg, self.theme.texture_color,
                                       center, r, width=2)
                cx, cy = center
                pygame.draw.line(bg, self.theme.texture_color,
                                 (0, cy), (WIDTH, cy))
                pygame.draw.line(bg, self.theme.texture_color,
                                 (cx, 0), (cx, HEIGHT))
            case Texture.COLUMNS:
                random.seed(42)
                c = self.theme.texture_color
                shades = [self._shade(c, 0.6), self._shade(c, 1.5)]
                x = 0
                while x < WIDTH:
                    pygame.draw.line(bg, random.choice(shades),
                                     (x, 0), (x, HEIGHT),
                                     width=random.randint(1, 4))
                    x += random.randint(6, 30)
            case _:
                pass
        return bg

    @staticmethod
    def _shade(rgb: RGB, factor: float) -> RGB:
        r, g, b = rgb
        return (min(255, int(r * factor)),
                min(255, int(g * factor)),
                min(255, int(b * factor)))

    def _apply_theme(self) -> None:
        self.theme = THEMES[self.theme_index]
        self.background = self._build_background()
        self.glow = self._build_glow()
