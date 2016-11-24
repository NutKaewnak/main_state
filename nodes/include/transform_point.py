import rospy
import tf


def transform_point(tf_listener, tf_points, destination_frame='base_link'):
        """
        Transform point from tf_points' frame_id to destination_frame
        :param tf_listener: (tf.TransformListener)
        :param tf_points: (geometry_msgs.msg.PointStamped)
        :param destination_frame: (string)
        :return: (geometry_msgs.msg.PointStamped), False if Error
        """
        tf_points.header.stamp = rospy.Time(0)
        try:
            tf_listener.waitForTransform(destination_frame, tf_points.header.frame_id, rospy.Time(0), rospy.Duration(1))
            point_out = tf_listener.transformPoint(destination_frame, tf_points)
            return point_out.point
        except (rospy.ROSInterruptException, tf.Exception):
            rospy.logwarn("Error while transforming a point from : " +
                          tf_points.header.frame_id + " to : " + destination_frame)
            return False

