from geometry_msgs.msg import PoseStamped

X_MAX = 0.66
X_MIN = 0.51
Y_MAX = 0.3
Y_MIN = -0.3
Z_MAX = 0.69
Z_MIN = 0.51


def is_in_range(pose_stamped):
    """

    :param pose_stamped: (geomerty_msgs.msg.PoseStamped)
    :return:
    """
    if X_MIN <= pose_stamped.x <= X_MAX:
        if Y_MIN <= pose_stamped.y <= Y_MAX:
            if Z_MIN <= pose_stamped.z <= Z_MAX:
                return True
    return