from drone import Move, ZoneMove, ConnectionMove


class TextPrinter:
    def format_turn(self, moves: list[Move]) -> str:
        output: list[str] = []
        for move in moves:
            if isinstance(move, ZoneMove):
                output.append(f"D{move.drone.drone_id}-{move.zone.name}")
            elif isinstance(move, ConnectionMove):
                output.append(
                        f"D{move.drone.drone_id}-{move.connection.name}")
        return " ".join(output)
