import pygame

from models import Map, Zone
from colors import RGB, COLORS, RAINBOW, RESET

WIDTH = 1600
HEIGHT = 900

MARGIN = 80

class Visualizer:
    def __init__(self, network: Map) -> None:
        pygame.init()

        self.network = network
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screen.fill((95, 116, 112))

                for zone in self.network.zones.values():
                    pygame.draw.circle(
                            self.screen,
                            COLORS.get(zone.color, (224, 226, 219)),
                            self._to_pixel(zone),
                            15)

                pygame.display.flip()
                self.clock.tick(30)

        pygame.quit()

    def _to_pixel(self, zone: Zone) -> tuple[int, int]:
        px = MARGIN + (zone.x - self.min_x) * self.scale
        py = MARGIN + (zone.y - self.min_y) * self.scale
        return (int(px), int(py))
