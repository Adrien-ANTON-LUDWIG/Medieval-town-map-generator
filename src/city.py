"""This module implements a city object, heart of the generation."""

import numpy as np
from shapely.geometry import MultiPolygon, LinearRing
from shapely.ops import cascaded_union

import src.tools as tools
from src.area import Area, Category
from src.regions import create_regions, create_houses, create_roads


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

        walls, regions = create_regions(population, density)

        self.areas = [Area(walls, Category.WALL)]

        houses = create_houses(walls, population)
        print(len(houses), 'houses')
        print(population / len(houses), 'hab/house')

        for region in regions:
            self.areas.append(Area(region, Category.LAND))

        streets = cascaded_union(MultiPolygon(houses))
        self.areas.append(Area(streets, Category.STREET))

        houses_area = np.average([house.area for house in houses])
        print('houses area before destruction : ', houses_area, 'm²')

        houses = [house for house in houses if house.area > 50]

        houses_area = np.average([house.area for house in houses])
        print('houses area after destruction : ', houses_area, 'm²')

        print(len(houses), 'houses')
        roads, houses = create_roads(regions, houses)
        print(len(houses), 'houses')

        for road in roads:
            self.areas.append(Area(road, Category.COMPOSITE))

        # houses = cut_houses(houses, roads)

        for house in houses:
            self.areas.append(Area(house, Category.HOUSE))

        walls = LinearRing(walls.exterior.coords).buffer(5, join_style=2)
        self.areas.append(Area(walls, Category.WALL))


if __name__ == '__main__':
    city = City(5000)
    tools.json(city, '/tmp/city.json')
