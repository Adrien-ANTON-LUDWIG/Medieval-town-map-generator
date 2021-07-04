"""This module enables to create doors."""
from shapely.geometry import Point
from shapely.ops import unary_union


def create_doors(walls, roads, land):
    """
    Computes doors at the intersection of walls and roads.

    Args:
        walls (Polygon): polygon representing the outer walls of the city.
        roads (Polygon): polygon representing the roads of the city.

    Returns:
        [Polygon]: list of polygons
    """

    land_and_walls = unary_union([land, walls])
    doors = [
        intersection.buffer(4, join_style=2)
        for intersection in walls.intersection(roads)
    ]

    new_doors = []
    for door in doors:
        new_door = [door]
        for x, y in door.exterior.coords:
            new_door.append(Point(x, y).buffer(2))
        new_doors.append(unary_union(new_door).difference(land_and_walls))

    return new_doors
