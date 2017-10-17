import zipfile

import geojson
from lxml import etree


def _kml_get_polygon(root):
    """Get Polygon GeoJSON from kml etree"""
    pattern = './/{*}LinearRing/{*}coordinates'
    try:
        s = root.find(pattern).text
    except AttributeError:
        return None
    cc = [(float(x), float(y)) for x, y in [p.split(',')[:2] for p in s.split()]]
    # make sure polygon is closed
    if cc[0] != cc[-1]:
        cc.append(cc[0])
    return geojson.Polygon(cc)


def _kml_get_point(root):
    """Get Point GeoJSON from kml etree"""
    pattern = './/{*}Point/{*}coordinates'
    try:
        s = root.find(pattern).text
    except AttributeError:
        return None
    c = [float(x) for x in s.split(',')[:2]]
    return geojson.Point(c)


def _kml_get_geometry(root):
    for func in [_kml_get_polygon, _kml_get_point]:
        gjson = func(root)
        if gjson is not None:
            return gjson
    raise ValueError('No Point or Polygon found.')


def read_kmz(kmzfile):
    """Extract doc.kml from KMZ file and parse geometry

    Returns
    -------
    dict
        GeoJSON mapping
    """
    with zipfile.ZipFile(kmzfile) as kmzf:
        with kmzf.open('doc.kml') as kmlf:
            return read_kml(kmlf)


def read_kml(kmlfile):
    """Read KML file and retrieve geometry

    Parameters
    ----------
    kmlfile : str
        path to KML file

    Returns
    -------
    dict
        GeoJSON mapping
    """
    tree = etree.parse(kmlfile)
    root = tree.getroot()
    return _kml_get_geometry(root)
