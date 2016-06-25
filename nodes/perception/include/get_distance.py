from math import hypot


def get_distance(point_a, point_b):
    return hypot((point_a[0] - point_b.point.x), (point_a[2] - point_b.point.y))
