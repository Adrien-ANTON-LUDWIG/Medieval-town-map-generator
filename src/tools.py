"""This module enables to save a city into a JSON file."""
from shapely.geometry import mapping, MultiPolygon
import fiona

SCHEMA = {
    'geometry': 'Polygon',
    'properties': {
        'category': 'int'
    },
}


def json(what, filename):
    """
    Saves a city object into a JSON file.
    :param what: city object.
    :param filename: location to save JSON file.
    """
    with fiona.open(filename, 'w', 'GeoJSON', SCHEMA) as c:
        for co in what.components():
            if isinstance(co.polygon(), MultiPolygon):
                for p in co.polygon():
                    c.write({
                        'geometry': mapping(p),
                        'properties': {
                            'category': co.category().value
                        },
                    })
            else:
                c.write({
                    'geometry': mapping(co.polygon()),
                    'properties': {
                        'category': co.category().value
                    },
                })
