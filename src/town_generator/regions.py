"""This module implements Voronoi's pavage to split the map into regions."""
from math import isqrt

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon


def create_regions(population, density):
    """
    Compute a varying number of regions.
    Regions' size depends on population and density.

    Args:
        population (int): population of the city.
        density (int): density of the city.

    Returns:
        [Polygon]: polygons representing regions.
    """
    superficy = population / density * 1000000
    side = isqrt(int(superficy))
    radius = side / 2
    isqrt_regions_number = 6

    points = np.array(
        [[x, y]
         for x in np.linspace(-radius, radius, isqrt_regions_number)
         for y in np.linspace(-radius, radius, isqrt_regions_number)])
    points += np.random.random((len(points), 2)) * (radius / 3)

    voronoi = Voronoi(points)

    regions = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    regions = [
        Polygon([voronoi.vertices[i] for i in region]) for region in regions
    ]

    zone = Polygon((2 * np.random.random(
        (8, 2)) - 1) * radius).convex_hull.buffer(radius / 2)
    regions = [region for region in regions if zone.contains(region)]

    return regions
