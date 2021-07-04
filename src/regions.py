"""This module implements Voronoi's pavage to split the map into regions."""
from math import isqrt

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union


def create_regions(population, density):
    """
    Compute a varying number of regions.
    Regions' size depends on population and density.
    :param population: population of the city.
    :param density: density of the city.
    :return: walls and regions polygons.
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


def create_houses(land, population):
    """
    Compute a varying number of houses.
    Houses' number and size depends on the city population.
    Houses are created from the center of the city  and not too close to the
    walls.
    :param land: walls of the city.
    :param population: population of the city.
    :return: polygons representing houses.
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


def create_roads(regions):
    """
    Computes main roads delimiting regions.
    :param regions: regions of the city.
    :return: computed roads.
    """
    return unary_union([
        LineString(region.exterior.coords).buffer(3, join_style=1)
        for region in regions
    ])


def create_walls(roads):
    """
    Compute walls from the perimeter of the roads.
    :param roads: main roads of the city.
    :return: walls of the city.
    """
    return roads.exterior.buffer(6,
                                 join_style=3).intersection(roads).buffer(0.5)


def cut_houses(houses, roads):
    """
    Cut previously generated houses (polygons) to avoid overlapping roads.
    :param houses: list of polygons representing houses.
    :param roads: polygon representing roads.
    :return: list of new polygons representing houses.
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
    :param house: list of polygons representing houses.
    :return: list of polygon representing houses.
    """
    return house.buffer(-1, join_style=2)
