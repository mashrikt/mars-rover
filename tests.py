from io import StringIO
import sys
import unittest
from unittest.mock import patch

from classes import Plateau, Rover
from mars_rover import main


class TestPlateau(unittest.TestCase):

    def test_create_plateau(self):
        plateau = Plateau(5, 5)
        self.assertEqual(plateau.x_min, 0)
        self.assertEqual(plateau.y_min, 0)
        self.assertEqual(plateau.x_max, 5)
        self.assertEqual(plateau.y_max, 5)

    def test_invalid_coordinates(self):
        with self.assertRaises(ValueError) as cm:
            Plateau(0, 0)
        self.assertEqual(
            'Incorrect value for the upper-right coordinates of the plateau.',
            str(cm.exception)
        )


class TestRover(unittest.TestCase):

    def setUp(self):
        self.plateau = Plateau(5, 5)

    def test_create_rover(self):
        rover = Rover('Mars Pathfinder', 1, 2, 'N', self.plateau)
        self.assertEqual(rover.name, 'Mars Pathfinder')
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 2)
        self.assertEqual(rover.direction, 'N')
        self.assertEqual(rover.plateau, self.plateau)

    def test_rover_above_top_right_plateau_point(self):
        with self.assertRaises(ValueError) as cm:
            Rover('Mars Pathfinder', 6, 5, 'N', self.plateau)
        self.assertEqual(
            'Provided coordinate is outside the plateau.',
            str(cm.exception)
        )

    def test_rover_below_bottom_left_plateau_point(self):
        with self.assertRaises(ValueError) as cm:
            Rover('Mars Pathfinder', 0, -1, 'N', self.plateau)
        self.assertEqual(
            'Provided coordinate is outside the plateau.',
            str(cm.exception)
        )

    def test_rover_direction_invalid(self):
        with self.assertRaises(ValueError) as cm:
            Rover('Mars Pathfinder', 1, 2, 'C', self.plateau)
        self.assertEqual(
            'Incorrect value for direction: C.',
            str(cm.exception)
        )

    def test_run_instruction_to_change_direction(self):
        rover = Rover('Mars Pathfinder', 1, 2, 'N', self.plateau)
        rover.run_instruction('L')
        self.assertEqual(rover.direction, 'W')
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 2)


    def test_run_instruction_to_move_forward(self):
        rover = Rover('Mars Pathfinder', 1, 2, 'N', self.plateau)
        rover.run_instruction('M')
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 3)
        self.assertEqual(rover.direction, 'N')

    def test_run_instruction_incorrect_input(self):
        rover = Rover('Mars Pathfinder', 1, 2, 'N', self.plateau)
        with self.assertRaises(ValueError) as cm:
            rover.run_instruction('X')
        self.assertEqual(
            'Incorrect instruction: X.',
            str(cm.exception)
        )

    def test_run_instruction_move_rover_outside_top_right_plateau_point(self):
        rover = Rover('Mars Pathfinder', 5, 5, 'N', self.plateau)
        with self.assertRaises(ValueError) as cm:
            rover.run_instruction('M')
        self.assertEqual(
            'Cannot process this move, as it would drive the rover out of the plateau.',
            str(cm.exception)
        )

    def test_run_instruction_move_rover_outside_bottom_left_plateau_point(self):
        rover = Rover('Mars Pathfinder', 0, 0, 'S', self.plateau)
        with self.assertRaises(ValueError) as cm:
            rover.run_instruction('M')
        self.assertEqual(
            'Cannot process this move, as it would drive the rover out of the plateau.',
            str(cm.exception)
        )


class TestIntegration(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def assert_stdout(self, fn, expected_output, mock_stdout):
        fn()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_run_from_file(self):
        testargs = ['mars_rover.py', 'input.txt']
        expected = 'Rover1:1 3 N\nRover2:5 1 E\n'
        with patch.object(sys, 'argv', testargs):
            self.assert_stdout(main, expected)

    def test_run_from_command_line(self):
        stdin_input = """Plateau:5 5
R1 Landing:1 1 N
R1 Instructions:MMMRM
R2 Landing:3 3 E
R2 Instructions:MRRM"""
        expected = 'R1:2 4 E\nR2:3 3 W\n'
        with patch.object(sys, 'stdin', StringIO(stdin_input)):
            self.assert_stdout(main, expected)
