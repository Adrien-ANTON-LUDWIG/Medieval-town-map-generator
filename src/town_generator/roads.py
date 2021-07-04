"""This module enables to create roads."""
from shapely.geometry import LinearRing
from shapely.ops import unary_union


def create_roads(regions):
    """
    Computes main roads delimiting regions.

    Args:
        regions ([Polygon]): regions of the city.

    Returns:
        Polygon: computed roads.
    """
    return unary_union([
        LinearRing(region.exterior.coords).buffer(3, join_style=2)
        for region in regions
    ])


def cut_roads(roads, land):
    """
    Resize the roads to stay inside the land.

    Args:
        roads (Polygon): polygon representing the roads.
        land (Polygon): polygon representing the land.
    Returns:
        Polygon: polygon representing the roads.
    """
    return roads.intersection(land)
