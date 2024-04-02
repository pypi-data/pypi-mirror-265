from shapely.geometry import LineString, MultiPolygon
from shapely.ops import polygonize, unary_union

def polygon_to_multipolygon_if_self_intersecting(polygon):
    """If a Polygon is invalid we try to convert it to a Multipolygon. If it is
    valid we just return it as it.

    This function assumes the Polygon is otherwise well formed, the only issue is
    that it is self-intersecting. That is, we assume the polygon is already 
    closed.
    """
    if polygon.is_valid:
        return polygon

    lr = LineString(polygon.exterior.coords[:])
    
    mls = unary_union(lr)
    mp = MultiPolygon(list(polygonize(mls)))
    return mp
