__author__ = 'nicole'
import rospy

from include.abstract_task import AbstractTask


class BasicFunctional(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('init BasicFunctional')
            self.change_state_with_subtask('movePassDoor', 'MovePassDoor')

        elif self.state is 'movePassDoor':
            if self.current_subtask.state is 'finish':
                self.subtask = self.change_state_with_subtask('moveToPickPlace', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.to_location('exit')

        elif self.state is 'moveToPickPlace':
            if self.current_subtask.state is 'finish':
                self.subtask = None
                rospy.loginfo('done recognize going to grab')
                self.change_state('grab')
                self.subtask = self.change_state_with_subtask('grab', 'Grab')
                # recognize both object
                # Grab.normal().grab(self.object)

        elif self.state is 'grab':
            if self.subtask is not None:
                self.subtask.grab_point(self.Object.position)
            # if self.object.isKnown is True:
                # if Grab.normal().state is STATE.SUCCESS:
                #   Grab.place().at(self.object.location)
            # elif self.object.isKnown is False
                # if Grab.normal().state is STATE.SUCCEED:
                #   Grab.place().at('bin')
            self.change_state('place')
            rospy.loginfo('change_state to Place')

        elif self.state is 'place':
            # if Grab.place().state is STATE.SUCCEED:
            if self.current_subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('10question', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.to_location('final')

        elif self.state is '10question':
            if self.current_subtask.state is 'finish':
                self.subtask = None
                # self.subtask = self.change_state_with_subtask('detect', 'DetectAndMoveToPeople')
                rospy.loginfo('change_state to detects /"SearchAndMoveToPeople/"')
                self.change_state('detect')

        elif self.state is 'detect':
            # answer random question
            # if self.current_subtask.state is 'finish':
                # self.subtask = self.change_state_with_subtask('exit', 'Answer several question')
            self.change_state('exit')
            rospy.loginfo('change_state to detects /"finish/"')

        elif self.state is 'exit':
            if self.current_subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('finish', 'LeaveArena')

        # Don't forget to add task to task_book
