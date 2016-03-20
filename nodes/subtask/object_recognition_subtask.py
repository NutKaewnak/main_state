__author__ = 'Nicole'
import rospy
import roslib
from object_recognition.srv import Recognize
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask
from shutil import copyfile


def object_status(status):
    if isinstance(status, int):
        if status == 1:
            return 'no_table'
        elif status == 2:
            return 'no_object'
        elif status == 3:
            return 'found_object'
        elif status == 4:
            return 'other_error'
        elif status == 5:
            return 'no_cloud_receive'


class ObjectRecognition(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.found_object = None
        self.delay = Delay()
        self.object_service = None
        self.input = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.delay.wait(150)
            self.found_object = []
            self.skillBook.get_skill(self, 'TurnNeck').turn(-0.1, 0)
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            try:
                self.object_service = rospy.ServiceProxy('object_recognition', Recognize)
            except rospy.ServiceException, e:
                rospy.loginfo("Object service call failed: %s" % e)

            self.input = self.object_service()
            if self.input.result is 'no_table':
                self.change_state('move_to_table')
            elif self.input.result is 'no_object':
                self.change_state('find_object')
            elif self.input.result is 'found_object':
                self.change_state('save_object')

        elif self.state is 'move_to_table':
            self.skill = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.skill.set_position(0.1, 0, 0)
            self.change_state('move_closer_to_shelf')

        elif self.state is 'move_closer_to_shelf':
            if self.skill.state is 'succeeded':
                self.input = self.make_self.input()
                if self.input.result is 'no_table':
                    self.change_state('move_to_table')
                elif self.input.result is 'no_object':
                    self.change_state('find_object')
                elif self.input.result is 'found_object':
                    self.change_state('save_object')

            elif self.skill.state is 'aborted':
                self.input = self.make_self.input()
                self.skill.set_position(-0.1, 0, 0)
                if self.input.result is 'no_object':
                    self.change_state('find_object')
                elif self.input.result is 'found_object':
                    self.change_state('save_object')

    def make_data(self):
        data = self.object_service()
        name_array = data.names
        time_stamp = data.clusters[0].header.stamp
        object_array = []
        counter = len(name_array)
        for i in range(counter):
            directory = roslib.packages.get_pkg_dir('object_recognition') + '/out/object_' + name_array[i] + '.png'
            new_directory = roslib.packages.get_pkg_dir('main_state') + '/detected_picture/' + name_array[i] + '.png'
            copyfile(directory, new_directory)
            object_array.append(DetectedObject(name_array[i], time_stamp, new_directory))

        out = ObjectDetectData(object_array, object_status(data.result))
        rospy.loginfo('Object detect service status: %s' % out.status)
        return out

    def get_object(self):
        return self.found_object


class ObjectDetectData():
    def __init__(self, object_array, status):
        self.object_array = object_array
        self.status = status

    def __str__(self):
        return 'status: ' + object_status(self.status) + ' ' + str(self.object_array)


class DetectedObject():
    def __init__(self, name, centroid, time_stamp, picture_directory):
        self.name = name
        self.time_stamp = time_stamp
        self.picture_directory = picture_directory

    def __str__(self):
        return str(self.name) + ', ' + str(self.time_stamp) + ', ' + str(self.centroid)
