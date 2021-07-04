"""This module enables to create towers."""
from shapely.geometry import Point


def create_towers(walls):
    """
    Computes towers on outer walls angles.

    Args:
        walls (Polygon): polygon representing the outer walls of the city.

    Returns:
        [Polygon]: list of polygons representing towers.
    """
    return [Point(x, y).buffer(3) for x, y in walls.exterior.coords]
