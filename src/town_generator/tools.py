"""This module enables to save a city into a JSON file."""
from shapely.geometry import mapping, MultiPolygon
import fiona

SCHEMA = {
    'geometry': 'Polygon',
    'properties': {
        'category': 'int'
    },
}


def json(city, filename):
    """
    Saves a city object into a JSON file.

    Args:
        city (City): city object.
        filename (string): location to save JSON file.
    """
    with fiona.open(filename, 'w', 'GeoJSON', SCHEMA) as c:
        for area in city.areas:
            if isinstance(area.polygon, MultiPolygon):
                for p in area.polygon:
                    c.write({
                        'geometry': mapping(p),
                        'properties': {
                            'category': area.category.value
                        },
                    })
            else:
                c.write({
                    'geometry': mapping(area.polygon),
                    'properties': {
                        'category': area.category.value
                    },
                })
