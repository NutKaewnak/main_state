import rospy
from include.abstract_subtask import AbstractSubtask
from include.transform_point import transform_point
from geometry_msgs.msg import PointStamped
import tf

__author__ = 'CinDy'


class DetectMiddleObject(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.detect_objects = None
        self.object_pos = None
        self.index = None
        self.tf_listener = tf.TransformListener()

    def perform(self, perception_data):
        if self.state is 'init':
            # check if skill is succeed
            self.detect_objects = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
            self.detect_objects.start()
            self.change_state('detecting')

        elif self.state is 'detecting':
            if self.detect_objects.state is 'finish':
                self.object_pos = self.detect_objects.objects
                for i in range(len(self.detect_objects.objects)):
                    obj = transform_point(self.tf_listener, self.detect_objects.objects[i], "map")

                    if -0.1 <= obj.point.y <= 0.1:
                        self.index = i
                        self.object_pos = transform_point(self.tf_listener, obj, "map")
                        self.change_state('finish')
                    else:
                        print 'object not in scope'
                        self.change_state('not_found')

            elif self.detect_objects.state is 'not_found':
                self.change_state('not_found')
