from geometry_msgs.msg import Point

X_MAX = 0.66
X_MIN = 0.51
Y_MAX = 0.3
Y_MIN = -0.3
Z_MAX = 0.69
Z_MIN = 0.51


def is_in_range(point):
    """

    :param point: (Point)
    :return: (Bool)
    """
    if X_MIN <= point.x <= X_MAX:
        if Y_MIN <= point.y <= Y_MAX:
            if Z_MIN <= point.z <= Z_MAX:
                return True
    return False


def find_new_available_point(point):
    """

    :param point: (Point)
    :return: (Point)
    """
    out_point = Point(point.x, point.y, point.z)
    while not is_in_range(out_point):
        if out_point.x > X_MAX:
            out_point.x -= 0.05
        elif out_point.x < X_MIN:
            out_point.x += 0.05

        if out_point.y > Y_MAX:
            out_point.y -= 0.05
        elif out_point.y < Y_MIN:
            out_point.y += 0.05

        if out_point.z > Z_MAX:
            out_point.z -= 0.05
        elif out_point.z < Z_MIN:
            out_point.z += 0.05

    return out_point
