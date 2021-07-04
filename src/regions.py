"""This module implements Voronoi's pavage to split the map into regions."""
from math import isqrt

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi
from shapely import ops
from shapely.geometry import Polygon, MultiPolygon, LineString
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
    # voronoi_plot_2d(voronoi)
    # plt.show()

    regions = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    regions = [
        Polygon([voronoi.vertices[i] for i in region]) for region in regions
    ]

    # for r in regions:
    #     plt.plot(*r.exterior.xy)

    # plt.show()

    zone = Polygon((2 * np.random.random(
        (8, 2)) - 1) * radius).convex_hull.buffer(radius / 2)
    regions = [region for region in regions if zone.contains(region)]

    # plt.plot(*zone.exterior.xy)
    # for region in regions:
    #     plt.plot(*region.exterior.xy)

    # plt.show()

    # 100 mètres entre les quartiers et les murs.
    walls = cascaded_union(MultiPolygon(regions).buffer(5, join_style=2))

    # plt.plot(*walls.exterior.xy)

    # for region in regions:
    #     plt.plot(*region.exterior.xy)

    # for tower in np.array(walls.exterior):
    #     plt.plot(*tower, '*')

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
    # voronoi_plot_2d(voronoi)
    # plt.show()

    houses = [r for r in voronoi.regions if -1 not in r and len(r) > 0]
    houses = [Polygon([voronoi.vertices[i] for i in house]) for house in houses]

    # for r in houses:
    #     plt.plot(*r.exterior.xy)

    # plt.show()

    houses = [
        house for house in houses
        if city_walls.buffer(-radius / 10, join_style=2).contains(house)
    ]

    # plt.plot(*region.exterior.xy)
    # for house in houses:
    #     plt.plot(*house.exterior.xy)

    # plt.show()

    return houses


def create_roads(regions, houses):
    """
    Computes main roads delimiting regions and updates the houses that overlap.
    :param regions: regions of the city.
    :param houses: houses of the city.
    :return: computed roads and updated houses.
    """
    roads_center = [LineString(region.exterior.coords) for region in regions]
    roads = [road.buffer(3, cap_style=3, join_style=3) for road in roads_center]

    new_houses = []
    for house in houses:
        new_houses += cut_house(house, roads_center, roads)

    return roads, new_houses


def cut_house(house, roads_center, roads):
    """

    :param houses:
    :param roads_center:
    :return:
    """
    new_houses = []
    intersected = False
    for i, road_center in enumerate(roads_center):
        other_roads_center = roads_center[:i] + roads_center[i + 1:]
        other_roads = roads[:i] + roads[i + 1:]
        if house.intersects(road_center):
            intersected = True
            splitted_houses = ops.split(house, road_center)

            for splitted_house in splitted_houses:
                diff = splitted_house.difference(roads[i])
                plt.plot(*splitted_house.exterior.xy)
                plt.plot(*diff.exterior.xy)
                plt.show()

                new_houses += cut_house(reduce_house(splitted_house),
                                        other_roads_center, other_roads)

            break

    if not intersected:
        new_houses.append(reduce_house(house))

    return new_houses


def reduce_house(house):
    return house.buffer(-1, join_style=2)
