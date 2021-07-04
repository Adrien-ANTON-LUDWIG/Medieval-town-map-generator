"""This module implements Voronoi's pavage to split the map into regions."""
from math import isqrt

import numpy as np
from scipy.spatial import Voronoi, Delaunay
from shapely.geometry import Polygon
from shapely.ops import unary_union


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
    isqrt_regions_number = 4

    points = np.array(
        [[x, y]
         for x in np.linspace(-radius, radius, isqrt_regions_number)
         for y in np.linspace(-radius, radius, isqrt_regions_number)])
    points += np.random.random((len(points), 2)) * (radius / 3)

    voronoi = Voronoi(points)
    delaunay = Delaunay(points)

    regions = [
        Polygon([delaunay.points[i]
                 for i in region])
        for region in delaunay.simplices
    ]

    roads_plans = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    roads_plans = [
        Polygon([voronoi.vertices[i]
                 for i in road_plan])
        for road_plan in roads_plans
    ]

    zone = unary_union(regions)
    roads_plans = [
        road_plan for road_plan in roads_plans if zone.intersects(road_plan)
    ]

    return regions, roads_plans
