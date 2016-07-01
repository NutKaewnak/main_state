from geometry_msgs.msg import Point

X_MAX_RIGHT = 0.66
X_MIN_RIGHT = 0.51
Y_MAX_RIGHT_1 = 0.07
Y_MIN_RIGHT_1 = -0.07
Y_MAX_RIGHT_2 = -0.21
Y_MIN_RIGHT_2 = -0.28
Z_MAX_RIGHT = 0.69
Z_MIN_RIGHT = 0.51

X_MAX_LEFT = 0.66
X_MIN_LEFT = 0.51
Y_MAX_LEFT = 0.28
Y_MIN_LEFT = 0.21
Z_MAX_LEFT = 0.69
Z_MIN_LEFT = 0.51


def is_in_right_range(point):
    """
    :param point: (Point)
    :return: (Bool)
    """
    if X_MIN_RIGHT <= point.x <= X_MAX_RIGHT:
        if (Y_MIN_RIGHT_1 <= point.y <= Y_MAX_RIGHT_1) or (Y_MIN_RIGHT_2 <= point.y <= Y_MAX_RIGHT_2) :
            if Z_MIN_RIGHT <= point.z <= Z_MAX_RIGHT:
                return True
    return False

def find_right_arm_nearest_area(point):
    output_point = point.y
    if abs(abs((Y_MAX_RIGHT_1 + Y_MIN_RIGHT_1)/2) - point) > abs(abs((Y_MAX_RIGHT_2 + Y_MIN_RIGHT_2)/2) - point):
        return "left_area"
    else :
        return "right_area"

def find_right_arm_available_point(point):
    """
    :param point: (Point)
    :return: (Point)
    """
    out_point = Point(point.x, point.y, point.z)
    while not is_in_right_range(out_point):
        if out_point.x > X_MAX_RIGHT:
            out_point.x -= 0.05
        elif out_point.x < X_MIN_RIGHT:
            out_point.x += 0.05

        nearest_area = find_right_arm_nearest_area(out_point.y)
        if(nearest_area == "left_area"):
            if out_point.y > Y_MAX_RIGHT_1:
                out_point.y -= 0.05
            elif out_point.y < Y_MIN_RIGHT_1:
                out_point.y += 0.05
        elif(nearest_area == "right_area"):
            if out_point.y > Y_MAX_RIGHT_2:
                out_point.y -= 0.05
            elif out_point.y < Y_MIN_RIGHT_2:
                out_point.y += 0.05

        if out_point.z > Z_MAX_RIGHT:
            out_point.z -= 0.05
        elif out_point.z < Z_MIN_RIGHT:
            out_point.z += 0.05
    return out_point

def is_in_left_range(point):
    """
    :param point: (Point)
    :return: (Bool)
    """
    if X_MIN_RIGHT <= point.x <= X_MAX_RIGHT:
        if Y_MIN_LEFT <= point.y <= Y_MAX_LEFT:
            if Z_MIN_RIGHT <= point.z <= Z_MAX_RIGHT:
                return True
    return False

def find_left_arm_available_point(point):
    """
    :param point: (Point)
    :return: (Point)
    """
    out_point = Point(point.x, point.y, point.z)
    while not is_in_right_range(out_point):
        if out_point.x > X_MAX_LEFT:
            out_point.x -= 0.05
        elif out_point.x < X_MIN_LEFT:
            out_point.x += 0.05

        if out_point.y > Y_MAX_LEFT:
            out_point.y -= 0.05
        elif out_point.y < Y_MIN_LEFT:
            out_point.y += 0.05

        if out_point.z > Z_MAX_LEFT:
            out_point.z -= 0.05
        elif out_point.z < Z_MIN_LEFT:
            out_point.z += 0.05
    return out_point