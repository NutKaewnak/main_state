__author__ = 'nicole'
from include.abstract_task import AbstractTask


class GPSR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            if self.state is 'init':
                self.set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)
                self.set_neck_angle_topic.publish(Vector3(0, 0, 0))
                self.change_state_with_subtask('movePassDoor', 'MovePassDoor')
                # self.change_state('movePassDoor')

        elif self.state is 'movePassDoor':
            self.subtask = self.change_state_with_subtask('doCategory2', 'ExtractObjectLocation')
            self.location = self.current_subtask.getLocation()

        elif self.state is 'doCategory2':
            if self.current_subtask.state is 'finish':
                self.change_state_with_subtask('exit', 'MoveToLocation')
                if self.current_subtask is not None:
                    self.current_subtask.to_location(self.location)
# Don't forget to add task to task_book