"""This module enables to create walls."""


def create_walls(land):
    """
    Compute walls from the perimeter of the roads.

    Args:
        land (Polygon): main roads of the city.

    Returns:
        Polygon: walls of the city.
    """
    return land.exterior.buffer(8, join_style=2).difference(land)
