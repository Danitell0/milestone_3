class ZoneType(Enum):
    NORMAL = auto()
    BLOCKED = auto()
    PRIORITY = auto()
    RESTRICTED = auto()

class Zone:
    def __init__(self):
        self.name: str = ""
        self.x: int = None
        self.y: int = None
        self.zone_type = ZoneType
        self.color: str = ""
        self.max_drones: int = None
