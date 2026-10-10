import pygame

from simulation import Simulation
from models import Map, Zone
from colors import COLORS, DEFAULT_ZONE_COLOR, RGB, RAINBOW

# animation
TURN_DELAY = 600
CONTROLS = ["Space: play / pause", "→: next turn"]

# window
WIDTH = 1800
HEIGHT = 1000

MARGIN = 80

# zone
RADIUS = 20


class Visualizer:
    def __init__(self, network: Map, sim: Simulation) -> None:
        pygame.init()

        # --------- Visual Control
        self.paused: bool = True
        self.last_step: int = 0

        self.sim = sim
        self.network = network
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 13)
        self.nb_font = pygame.font.Font(None, 20)
        self.counter_font = pygame.font.Font(None, 50)

        # ---------- Map scale compute
        self.min_x = min(zone.x for zone in network.zones.values())
        self.max_x = max(zone.x for zone in network.zones.values())
        self.min_y = min(zone.y for zone in network.zones.values())
        self.max_y = max(zone.y for zone in network.zones.values())
        self.usable_w = WIDTH - 2 * MARGIN
        self.usable_h = HEIGHT - 2 * MARGIN
        # max() in case of 0
        self.range_x = max((self.max_x - self.min_x), 1)
        self.range_y = max((self.max_y - self.min_y), 1)
        self.scale = min((self.usable_w / self.range_x),
                         (self.usable_h / self.range_y))

        pygame.display.set_caption("Fly-in project by danmorei")

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
                            self.sim.step()
                    elif event.key == pygame.K_SPACE:
                        if not self.sim.is_finished():
                            self.paused = not self.paused

            # time block
            now = pygame.time.get_ticks()
            if (not self.paused
                    and not self.sim.is_finished()
                    and now - self.last_step >= TURN_DELAY):
                self.sim.step()
                self.last_step = now

            # drawing block
            self.screen.fill((95, 116, 112))
            self._draw_hud()
            if self.sim.is_finished():
                turn_text = f"Finished in {self.sim.turn} turns"
            else:
                turn_text = f"Turn {self.sim.turn}"
            display_text = self.counter_font.render(turn_text,
                                                    True,
                                                    COLORS["black"])
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
        # drawing the links
        for link in self.network.connections.values():
            pygame.draw.line(
                    self.screen,
                    COLORS["gray"],
                    self._to_pixel(link.zone_a),
                    self._to_pixel(link.zone_b),
                    5)

        # drawing the zones
        for zone in self.network.zones.values():
            px, py = self._to_pixel(zone)
            pygame.draw.circle(
                    self.screen,
                    self._zone_rgb(zone),
                    (px, py),
                    RADIUS)
            text = self.font.render(zone.name, True, COLORS["black"])
            rect = text.get_rect(
                    center=(px, py + RADIUS + 10))
            self.screen.blit(text, rect)

    def _draw_drones(self) -> None:
        counts: dict[str, int] = {}

        for drone in self.sim.active_drones:
            if drone.zone is None and drone.connection:
                x1, y1 = self._to_pixel(drone.connection.zone_a)
                x2, y2 = self._to_pixel(drone.connection.zone_b)
                midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
                pygame.draw.circle(
                        self.screen,
                        COLORS["black"],
                        midpoint,
                        6
                        )
                continue
            if drone.zone is None:
                continue
            counts[drone.zone.name] = counts.get(drone.zone.name, 0) + 1

        for name, count in counts.items():
            zone = self.sim.network.zones[name]
            pygame.draw.circle(
                    self.screen,
                    COLORS["black"],
                    self._to_pixel(zone),
                    6
                    )
            text = self.nb_font.render(f"x{count}", True, COLORS["black"])
            px, py = self._to_pixel(zone)
            rect = text.get_rect(center=(px + RADIUS + 10, py - RADIUS))
            self.screen.blit(text, rect)

    def _draw_hud(self) -> None:
        line_height = self.nb_font.get_linesize()
        start_y = HEIGHT - 20 - len(CONTROLS) * line_height
        for i, command in enumerate(CONTROLS):
            y = start_y + i * line_height
            text = self.nb_font.render(command,
                                       True,
                                       COLORS["black"])
            self.screen.blit(text, (20, y))

    def _zone_rgb(self, zone: Zone) -> RGB:
        if zone.color == "rainbow":
            return RAINBOW[(pygame.time.get_ticks() // 300) % len(RAINBOW)]
        return COLORS.get(zone.color or "", DEFAULT_ZONE_COLOR)
