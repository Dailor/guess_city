import math

def get_scale(GeoObj: dict):
    obj_rect = map(lambda x: x.split(), GeoObj['boundedBy']['Envelope'].values())
    (x1, y1), (x2, y2) = map(lambda x: map(float, x), obj_rect)
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx, dy  # * 3.218 * 10**-1
