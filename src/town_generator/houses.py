"""This module functions to create houses."""

from math import isqrt

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon


def create_houses(land, population):
    """
    Compute a varying number of houses.
    Houses' number and size depends on the city population.
    Houses are created from the center of the city  and not too close to the
    walls.

    Args:
        land (Polygon): walls of the city.
        population (int): population of the city.

    Returns:
        [Polygon]: polygons representing houses.
    """
    houses_number = int(population / 1.5)
    isqrt_houses_number = isqrt(houses_number)

    (min_x, min_y, max_x, max_y) = land.bounds

    radius = ((max_x - min_x) + (max_y - min_y)) / 2

    points = np.array([[x, y]
                       for x in np.linspace(min_x, max_x, isqrt_houses_number)
                       for y in np.linspace(min_y, max_y, isqrt_houses_number)])
    points += np.random.random((len(points), 2)) * (radius / 3)

    voronoi = Voronoi(points)

    houses = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    houses = [Polygon([voronoi.vertices[i] for i in house]) for house in houses]

    houses = [
        house for house in houses
        if land.buffer(-radius / 10, join_style=2).contains(house)
    ]

    return houses


def cut_houses(houses, roads):
    """
    Cut previously generated houses (polygons) to avoid overlapping roads.

    Args:
        houses ([Polygon]): list of polygons representing houses.
        roads (Polygon): polygon representing roads.

    Returns:
        [Polygon]: list of new polygons representing houses.
    """

    new_houses = []
    for house in houses:
        diff = house.difference(roads)

        if isinstance(diff, Polygon):
            new_houses.append(diff)
        else:
            for d in diff:
                new_houses.append(d)

    return new_houses


def reduce_house(house):
    """
    Scales down the houses.

    Args:
        house ([Polygon]): list of polygons representing houses.

    Returns:
        [Polygon]: list of polygon representing houses.
    """
    return house.buffer(-1, join_style=2)
