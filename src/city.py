"""This module implements a city object, heart of the generation."""
from shapely.geometry import Polygon

import src.tools as tools
from src.area import Area, Category


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
        self.districts = []

    @staticmethod
    def components():
        poly = Polygon([(0, 0), (2, 0), (1, 2), (0, 0)])
        area = Area(poly, Category.HOUSE)
        return [area]


if __name__ == '__main__':
    city = City(5000)
    tools.json(city, '/tmp/city.json')
