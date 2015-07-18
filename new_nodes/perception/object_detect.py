__author__ = 'Nicole'

import rospy
import roslib
# from std_msgs.msg import String
from geometry_msgs.msg import Point
from object_detection.msg import ObjectDetection
from include.abstract_perception import AbstractPerception
from include.devices import Devices


def object_status(status):
    if isinstance(status, int):
        if status == 1:
            return 'no_table'
        elif status == 2:
            return 'no_object'
        elif status == 3:
            return 'found_object'
        elif status == 4 or status == 5:
            return 'other_error'


class ObjectDetect(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        # rospy.Subscriber('/tabletop_object_detection', ObjectDetection, self.callback_object_point)

    def callback_object_point(self, data):
        name_array = data.names
        centroid_array = data.centroids
        time_stamp = data.table.header.stamp
        object_array = []
        if len(name_array) == len(centroid_array):
            counter = len(name_array)
            for i in range(counter):
                directory = roslib.packages.get_pkg_dir('object_recognition') + '/out/object_' + name_array[i] + '.png'
                object_array.append(DetectedObject(name_array[i], centroid_array[i], time_stamp, directory))

        self.broadcast(Devices.OBJECT, ObjectDetectData(object_array, object_status(data.result)))


class ObjectDetectData():
    def __init__(self, object_array, status):
        self.object_array = object_array
        self.status = status

    def __str__(self):
        return 'status: ' + object_status(self.status) + ' ' + str(self.object_array)


class DetectedObject():
    def __init__(self, name, centroid, time_stamp, picture_directory):
        self.name = name
        self.centroid = centroid
        self.time_stamp = time_stamp
        self.picture_directory = picture_directory

    def __str__(self):
        return str(self.name) + ', ' + str(self.time_stamp) + ', ' + str(self.centroid)