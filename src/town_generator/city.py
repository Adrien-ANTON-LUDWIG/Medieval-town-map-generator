"""This module implements a city object, heart of the generation."""

import numpy as np
from shapely.geometry import MultiPolygon
from shapely.ops import cascaded_union, unary_union

import src.town_generator.tools as tools
from src.town_generator.area import Area, Category
from src.town_generator.doors import create_doors
from src.town_generator.houses import create_houses, cut_houses, reduce_houses
from src.town_generator.regions import create_regions
from src.town_generator.roads import create_roads, cut_roads
from src.town_generator.towers import create_towers
from src.town_generator.walls import create_walls
from src.town_generator.gardens import create_gardens
from src.town_generator.university import create_universities


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
        regions, roads_plans = create_regions(population, density)
        land = unary_union(regions)

        for region in regions:
            self.areas.append(Area(region, Category.LAND))

        walls = create_walls(land)
        self.areas.append(Area(walls, Category.WALL))

        roads = create_roads(roads_plans)

        doors = create_doors(walls, roads, land)
        print(len(doors))
        for door in doors:
            self.areas.append(Area(door, Category.DOOR))

        roads = cut_roads(roads, land)
        # roads = roads.difference(walls)
        self.areas.append(Area(roads, Category.ROAD))

        towers = create_towers(walls)
        for tower in towers:
            self.areas.append(Area(tower, Category.WALL))

        houses, fields = create_houses(land, population)
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

        houses, universities = create_universities(houses)
        for university in universities:
            self.areas.append(Area(university, Category.UNIVERSITY))

        houses = reduce_houses(houses)
        for house in houses:
            self.areas.append(Area(house, Category.HOUSE))

        gardens = create_gardens(houses, streets)
        for garden in gardens:
            self.areas.append(Area(garden, Category.GARDEN))

        fields = cut_houses(fields, roads)
        for field in fields:
            self.areas.append(Area(field, Category.FIELD))


if __name__ == '__main__':
    city = City(5000)
    tools.json(city, '/tmp/city.json')
