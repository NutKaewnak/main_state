#! /usr/bin/python

import rospy
import roslib
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

DEFAULT_SAVE_DIR = roslib.packages.get_pkg_dir('main_state')+'/picture/'
bridge = CvBridge()


def save_image(image, image_path=DEFAULT_SAVE_DIR+'test.png'):
    """

    :param image: (sensor_msgs.msg.Image)
    :param image_path: (str)
    :return: (None)
    """
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(image, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        cv2.imwrite(image_path, cv2_img)


def image_subscriber(data):
    save_image(data, 'test')


if __name__ == '__main__':
    rospy.init_node('image_saver', anonymous=True)
    rospy.Subscriber('/image', Image, image_subscriber)
    rospy.spin()
