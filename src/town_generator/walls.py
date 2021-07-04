"""This module enables to create walls."""


def create_walls(roads):
    """
    Compute walls from the perimeter of the roads.
    :param roads: main roads of the city.
    :return: walls of the city.
    """
    return roads.exterior.buffer(6,
                                 join_style=3).intersection(roads).buffer(0.5)
