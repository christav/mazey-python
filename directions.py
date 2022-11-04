# Class and enumeration describing directions you can move in a maze

from enum import Enum

# A single direction - includes x, y deltas and a bitmask

class Direction:
    def __init__(self, dx, dy, bit_num):
        self.dx = dx
        self.dy = dy
        self.mask = 1 << bit_num if bit_num != -1 else 0

# All our directions

class Directions(Enum):
    STATIONARY = Direction(0, 0, -1)
    UP = Direction(0, -1, 0)
    DOWN = Direction(0, 1, 1)
    LEFT = Direction(-1, 0, 2)
    RIGHT = Direction(1, 0, 3)

    @staticmethod
    def all():
        yield Directions.UP
        yield Directions.LEFT
        yield Directions.DOWN
        yield Directions.RIGHT

    @staticmethod
    def opposite(d):
        return {
            Directions.STATIONARY: Directions.STATIONARY,
            Directions.UP: Directions.DOWN,
            Directions.DOWN: Directions.UP,
            Directions.LEFT: Directions.RIGHT,
            Directions.RIGHT: Directions.LEFT
        }.get(d, Directions.STATIONARY)
