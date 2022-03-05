import os
import sys

from classes import Plateau, Rover
from config import ROVER_COMMANDS


def main():
    file = None
    plateau = None
    rover = None

    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        # redirect stdin to the file
        file = open(sys.argv[1], 'r')
        sys.stdin = file


    for line in sys.stdin:
        command = line.strip()
        if not plateau:
            plateau = initialize_plateau(command)
        else:
            rover = rover_command(command, rover, plateau)

    if file:
        sys.stdin = sys.__stdin__
        file.close()


def initialize_plateau(command):
    if not command.startswith('Plateau:'):
        raise ValueError('Have to initialize the plateau first.')
    x, y = command.split('Plateau:')[1].split(' ')
    return Plateau(int(x), int(y))


def rover_command(command, rover, plateau):
    name, action = command.split(' ', 1)
    command, instructions = action.split(':')
    if command == ROVER_COMMANDS.LANDING.value:
        x, y, direction = instructions.split(' ')
        rover = Rover(name, int(x), int(y), direction, plateau)
    elif command == ROVER_COMMANDS.INSTRUCTION.value:
        if rover.name != name:
            raise ValueError('Incorrect sequence of commands for rover.')
        for instruction in instructions:
            rover.run_instruction(instruction)
        print(rover)
    return rover


if __name__ == '__main__':
    main()
