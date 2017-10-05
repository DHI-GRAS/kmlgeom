import zipfile

from lxml import etree


def read_kmz(kmzfile):
    with zipfile.ZipFile(kmzfile) as kmzf:
        with kmzf.open('doc.kml') as kmlf:
            return read_kml(kmlf)


def kml_get_polygon(root):
    """Get Polygon GeoJSON from kml etree"""
    pattern = './/{*}LinearRing/{*}coordinates'
    try:
        s = root.find(pattern).text
    except AttributeError:
        return {}
    cc = [(float(x), float(y)) for x, y in [p.split(',')[:2] for p in s.split()]]

    # make sure polygon is closed
    if cc[0] != cc[-1]:
        cc.append(cc[0])
    gjson = {"type": "Polygon", "coordinates": [cc]}
    return gjson


def kml_get_point(root):
    """Get Point GeoJSON from kml etree"""
    pattern = './/{*}Point/{*}coordinates'
    try:
        s = root.find(pattern).text
    except AttributeError:
        return {}
    c = [float(x) for x in s.split(',')[:2]]
    gjson = {"type": "Point", "coordinates": c}
    return gjson


def kml_get_geometry(root):
    for func in [kml_get_polygon, kml_get_point]:
        gjson = func(root)
        if gjson:
            return gjson
    raise ValueError('No Point or Polygon found.')


def read_kml(kmlfile):
    """Read KML file and retrieve geometry

    Parameters
    ----------
    kmlfile : str
        path to KML file

    Returns
    -------
    str : GeoJSON string
    """
    tree = etree.parse(kmlfile)
    root = tree.getroot()
    return kml_get_geometry(root)
