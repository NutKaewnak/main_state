from math import sqrt


def get_distance(point_a, point_b):
    return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)
