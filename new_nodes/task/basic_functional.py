from subprocess import call
from geometry_msgs.msg import Vector3
from include.delay import Delay

__author__ = 'nicole'
import rospy
from include.abstract_task import AbstractTask


class BasicFunctional(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)
        set_neck_angle_topic.publish(Vector3())
        self.state = 'place'
        call(["espeak", "-ven+f4", 'init basic functionality.', "-s 120"])

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('init BasicFunctional')
            self.change_state_with_subtask('movePassDoor', 'MovePassDoor')
            call(["espeak", "-ven+f4", 'move pass door.', "-s 120"])


        elif self.state is 'movePassDoor':
            if self.current_subtask.state is 'finish':
                self.subtask = self.change_state_with_subtask('moveToPickPlace', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.to_location('PickPlace')
                    call(["espeak", "-ven+f4", 'going to pick and place.', "-s 120"])

        elif self.state is 'moveToPickPlace':
            if self.current_subtask.state is 'finish':
                self.subtask = None
                rospy.loginfo('done recognize going to grab')
                self.timer = Delay()
                self.timer.wait(23)
                self.subtask = self.change_state('recognize')
                # recognize both object
                # Grab.normal().grab(self.object)

        elif self.state is 'recognize':
            # fail of course
            if not self.timer.is_waiting():
                # self.change_state('grab')
                call(["espeak", "-ven+f4", 'I cannot found any object.', "-s 120"])
                self.subtask = self.subtaskBook.get_subtask('MoveToLocation')
                self.subtask.to_location('notFound')
                self.change_state('notFound')

        elif self.state is 'notFound':

            # if self.subtask is not None:
                # self.subtask.grab_point(self.Object.position)
            call(["espeak", "-ven+f4", 'I will do Avoid That.', "-s 120"])
            self.change_state('place')
            rospy.loginfo('change_state to Place')

        elif self.state is 'place':
            # if Grab.place().state is STATE.SUCCEED:
            # if self.current_subtask.state is 'finish':
                # self.subtask = None
            self.subtask = self.change_state_with_subtask('QuestionAnswer', 'MoveToLocation')
            call(["espeak", "-ven+f4", 'I will do QuestionAnswer', "-s 120"])
            if self.subtask is not None:
                self.subtask.to_location('detect')

        elif self.state is 'QuestionAnswer':
            if self.current_subtask.state is 'finish':
                call(["espeak", "-ven+f4", 'question answering', "-s 120"])
                self.subtask = self.change_state_with_subtask('detect', 'DetectAndMoveToPeople')
                rospy.loginfo('change_state to detects /"SearchAndMoveToPeople/"')
                self.change_state('detect')

        elif self.state is 'detect':
            # answer random question
            if self.current_subtask.state is 'finish':
                self.subtask = self.change_state_with_subtask('exit', 'QuestionAnswer')
            self.change_state('exit')
            rospy.loginfo('change_state to detects /"finish/"')

        elif self.state is 'exit':
            if self.current_subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('finish', 'LeaveArena')

        # Don't forget to add task to task_book
