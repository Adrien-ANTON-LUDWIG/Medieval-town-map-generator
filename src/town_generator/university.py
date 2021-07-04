"""This module creates universities into the city"""
import random


def create_universities(houses):
    """
    this function creates universities
    Args:
        houses ([Polygon]): houses of the city
    Returns:
        [Polygon], [Polygon]: new list of houses, universities
    """
    universities = []
    new_houses = []

    for house in houses:
        if random.randint(0, 35) == 1:
            universities.append(house)
        else:
            new_houses.append(house)
    return new_houses, universities
