"""This module contains the functional tests of our medieval town generator.

There are only a few tests because the quality of the generation is subjective,
so it can not be automated.
"""
from src.town_generator import tools, viewer
from src.town_generator.city import City


def test_city(n):
    city = City(n)

    try:
        tools.json(city, './resources/test_city.json')
        viewer.display('./resources/test_city.json')
    except:
        print('Test with', n, 'cities failed!')
        raise


def test_little_city():
    test_city(500)


def test_normal_city():
    test_city(5000)


def test_big_city():
    test_city(50000)
