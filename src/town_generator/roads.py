"""This module enables to create roads."""
from shapely.geometry import LineString
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
        LineString(region.exterior.coords).buffer(3, join_style=1)
        for region in regions
    ])
