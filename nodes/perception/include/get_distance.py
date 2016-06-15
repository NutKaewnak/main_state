from math import hypot


def get_distance(point_a, point_b):
    return hypot((point_a.x - point_b.x), (point_a.y - point_b.y))
