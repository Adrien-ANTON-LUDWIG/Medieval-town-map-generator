"""This module implements Voronoi's pavage to split the map into regions."""
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from math import isqrt

from shapely.ops import cascaded_union


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
    voronoi_plot_2d(voronoi)
    # plt.show()

    regions = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    regions = [
        Polygon([voronoi.vertices[i] for i in region]) for region in regions
    ]

    for r in regions:
        plt.plot(*r.exterior.xy)

    # plt.show()

    zone = Polygon((2 * np.random.random(
        (8, 2)) - 1) * radius).convex_hull.buffer(radius / 2)
    regions = [region for region in regions if zone.contains(region)]

    plt.plot(*zone.exterior.xy)
    for region in regions:
        plt.plot(*region.exterior.xy)

    # plt.show()

    # 100 mètres entre les quartiers et les murs.
    walls = cascaded_union(MultiPolygon(regions).buffer(5, join_style=2))

    plt.plot(*walls.exterior.xy)

    for region in regions:
        plt.plot(*region.exterior.xy)

    for tower in np.array(walls.exterior):
        plt.plot(*tower, '*')

    # plt.show()

    return walls, regions


def create_houses(city_walls, population):
    """
    Compute a varying number of houses.
    Houses' number and size depends on the city population.
    Houses are created from the center of the city  and not too close to the
    walls.
    :param city_walls: walls of the city.
    :param population: population of the city.
    :return: polygons representing houses.
    """
    houses_number = int(population / 1.5)
    isqrt_houses_number = isqrt(houses_number)

    (min_x, min_y, max_x, max_y) = city_walls.bounds

    diff_x = max_x - min_x
    diff_y = max_y - min_y
    radius = (diff_x + diff_y) / 2

    delta_x = diff_x / 20
    delta_y = diff_y / 20

    min_x += delta_x
    max_x -= delta_x
    min_y += delta_y
    max_y -= delta_y

    points = np.array([[x, y]
                       for x in np.linspace(min_x, max_x, isqrt_houses_number)
                       for y in np.linspace(min_y, max_y, isqrt_houses_number)])
    points += np.random.random((len(points), 2)) * (radius / 3)

    voronoi = Voronoi(points)
    voronoi_plot_2d(voronoi)
    # plt.show()

    houses = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    houses = [Polygon([voronoi.vertices[i] for i in house]) for house in houses]

    for r in houses:
        plt.plot(*r.exterior.xy)

    # plt.show()

    houses = [
        house for house in houses
        if city_walls.buffer(-radius / 10, join_style=2).contains(house)
    ]

    # plt.plot(*region.exterior.xy)
    for house in houses:
        plt.plot(*house.exterior.xy)

    # plt.show()

    return houses
