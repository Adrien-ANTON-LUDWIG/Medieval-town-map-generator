"""This module contains the unit tests of the towers' module."""
from matplotlib.patches import Polygon

from src.town_generator.towers import create_towers


def test_tower_number():
    square = Polygon([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0],
                      [0.0, 0.0]])
    towers = create_towers(square)
    assert len(towers) == 4
