from dataclasses import dataclass
from enum import Enum


class ROVER_COMMANDS(Enum):
    LANDING = 'Landing'
    INSTRUCTION = 'Instructions'


@dataclass
class Coordinate:
    x: int
    y: int


DIRECTION_TO_DELTA_COORDINATES = {
    'N': Coordinate(0, 1),
    'E': Coordinate(1, 0),
    'W': Coordinate(-1, 0),
    'S': Coordinate(0, -1),
}


DIRECTION_TO_DEGREE = {
    'N': 90,
    'E': 0,
    'W': 180,
    'S': 270,
}

DEGREE_TO_DIRECTION = {v: k for k, v in DIRECTION_TO_DEGREE.items()}

SIDE_TO_ANGLE = {
    'L': 90,
    'R': -90,
}

MOVE_FORWARD_INSTRUCTION = 'M'
