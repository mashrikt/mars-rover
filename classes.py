from dataclasses import dataclass

from config import (DEGREE_TO_DIRECTION, DIRECTION_TO_DEGREE, DIRECTION_TO_DELTA_COORDINATES,
    MOVE_FORWARD_INSTRUCTION, SIDE_TO_ANGLE)


@dataclass
class Plateau:
    x_min = 0
    y_min = 0
    x_max: int
    y_max: int

    def __post_init__(self):
        if self.x_max <= self.x_min or self.y_max <= self.y_min:
            raise ValueError(f'Incorrect value for the upper-right coordinates of the plateau.')

    def is_coordinate_inside_plateau(self, x, y):
        is_x_inside_plateau = x >= self.x_min and x <= self.x_max
        is_y_inside_plateau = y >= self.y_min and y <= self.y_max
        return is_x_inside_plateau and is_y_inside_plateau


@dataclass
class Rover:
    name: str
    x: int
    y: int
    direction: str
    plateau: Plateau

    def __post_init__(self):
        if not self.plateau.is_coordinate_inside_plateau(self.x, self.y):
            raise ValueError('Provided coordinate is outside the plateau.')
        if self.direction not in DIRECTION_TO_DELTA_COORDINATES.keys():
            raise ValueError(f'Incorrect value for direction: {self.direction}.')

    def run_instruction(self, instruction):
        if instruction in SIDE_TO_ANGLE.keys():
            self._change_direction(instruction)
        elif instruction == MOVE_FORWARD_INSTRUCTION:
            self._move_forward()
        else:
            raise ValueError(f'Incorrect instruction: {instruction}.')


    def _change_direction(self, direction_of_rotation):
        angle_of_direction = DIRECTION_TO_DEGREE[self.direction]
        theta = SIDE_TO_ANGLE[direction_of_rotation]
        new_angle = angle_of_direction + theta
        # normalize the angle between 0 to 360
        new_normalized_angle = (new_angle + 360) % 360
        self.direction = DEGREE_TO_DIRECTION[new_normalized_angle]

    def _move_forward(self):
        delta_coordinate = DIRECTION_TO_DELTA_COORDINATES[self.direction]
        new_x = self.x + delta_coordinate.x
        new_y = self.y + delta_coordinate.y
        if not self.plateau.is_coordinate_inside_plateau(new_x, new_y):
            raise ValueError('Cannot process this move, as it would drive the rover out of the plateau.')
        self.x = new_x
        self.y = new_y

    def __str__ (self):
        return f"{self.name}:{self.x} {self.y} {self.direction}"
