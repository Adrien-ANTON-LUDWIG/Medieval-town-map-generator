"""This module creates gardens"""
import random
from math import sqrt


def has_garden(house, streets):
    """ Determines if a house has a garden or not. We consider that the center
     of a town is in (0,0) : Not necessarily at the center of the city. The
     chances of a house to get a garden are smaller next to the center than
     far from it.

     Args:
        house (Polygon): the concerned house
        streets (Polygon): the streets of the city

    """
    (min_x, min_y, max_x, max_y) = streets.bounds
    (min_house_x, min_house_y, max_house_x, max_house_y) = house.bounds

    house_center_x = (min_house_x + max_house_x) / 2
    house_center_y = (min_house_y + max_house_y) / 2

    radius = (abs(min_x) + abs(min_y) + abs(max_x) + abs(max_y)) / 4
    dist_to_zero = sqrt(house_center_x**2 + house_center_y**2)

    rand = random.random()

    if 0 <= dist_to_zero <= radius / 3:
        return rand < 0.2

    if radius / 3 < dist_to_zero <= 2 * radius / 3:
        return rand < 0.5

    #else (2 * sum_streets / 3 < sum_house and sum_house <= sum_streets)
    return rand < 0.95


def create_gardens(houses, streets):
    """ Creates a garden for each existing house on the map
    Args:
        houses ([Polygon]): houses of the city
    Returns:
        [Polygons]: list of the gardens
    """
    gardens = []
    for house in houses:
        if has_garden(house, streets):
            garden = house.buffer(-(house.length / 15), join_style=2)
            gardens.append(garden)
    return gardens
