"""This module implements a city object, heart of the generation."""

import numpy as np
from shapely.geometry import MultiPolygon
from shapely.ops import cascaded_union, unary_union

import src.tools as tools
from src.area import Area, Category
from src.regions import create_regions, create_houses, create_roads, cut_houses, reduce_house, create_walls


class City:
    """
    Implements the city object. It's the top of the hierarchy.
    It contains areas.
    """

    def __init__(self,
                 population,
                 density=10000,
                 has_walls=False,
                 has_castle=False,
                 has_river=False):
        self.population = population

        # 10 000 ha/km2 par défaut mais peut baisser à 2000 ha/km2 avec les
        # champs et monter à 30000 ha/km2
        self.density = density

        self.has_walls = has_walls
        self.has_castle = has_castle
        self.has_river = has_river

        self.areas = []
        regions = create_regions(population, density)
        land = unary_union(regions)

        for region in regions:
            self.areas.append(Area(region, Category.LAND))

        roads = create_roads(regions)

        walls = create_walls(roads)
        self.areas.append(Area(walls, Category.WALL))

        roads = roads.difference(walls)
        self.areas.append(Area(roads, Category.ROAD))

        houses = create_houses(land, population)
        print(len(houses), 'houses')
        houses_area = np.average([house.area for house in houses])
        print('houses area before split : ', houses_area, 'm²')

        houses = cut_houses(houses, roads)
        print(len(houses), 'houses')
        houses_area = np.average([house.area for house in houses])
        print('houses area after split : ', houses_area, 'm²')

        houses = [house for house in houses if house.area > 30]
        print(len(houses), 'houses')
        houses_area = np.average([house.area for house in houses])
        print('houses area after destruction : ', houses_area, 'm²')

        print(population / len(houses), 'hab/house')

        streets = cascaded_union(MultiPolygon(houses))
        self.areas.append(Area(streets, Category.STREET))

        houses = [reduce_house(house) for house in houses]
        for house in houses:
            self.areas.append(Area(house, Category.HOUSE))


if __name__ == '__main__':
    city = City(5000)
    tools.json(city, '/tmp/city.json')
