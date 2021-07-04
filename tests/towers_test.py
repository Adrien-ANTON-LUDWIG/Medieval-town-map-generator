"""This module contains the unit tests of the towers' module.

This is more of an example of unit tests.
As the code depends mostly on other libraries,
not so much test are needed.
"""

from matplotlib.patches import Polygon

from src.town_generator.towers import create_towers


def test_tower_number():
    square = Polygon([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0],
                      [0.0, 0.0]])
    towers = create_towers(square)
    assert len(towers) == 4
