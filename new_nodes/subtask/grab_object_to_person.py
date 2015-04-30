__author__ = 'nicole'

import rospy

from include.abstract_subtask import AbstractSubtask


class GrabObjectToPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.object = None
        self.personName = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.object = None
            self.personName = None

        elif self.state is 'start':
            self.subtask = self.subtaskBook.get_subtask('MoveToLocation')
            self.subtask.to_location('kitchenTable')
            self.change_state('moveToKitchenTable')

        elif self.state is 'moveToKitchenTable':
            if self.current_subtask.state is 'succeed':
                # rospy.wait_for_service('mukService')
                # try:
                #     add_two_ints = rospy.ServiceProxy('mukService', mukService)
                #     self.objPos = mukService(self.object)
                # except rospy.ServiceException, e:
                #     print "Service call failed: %s"%e
                self.change_state('foundObject')
                rospy.loginfo('foundObject')
                # elif self.objPos is None:
                #     self.change_state('objectNotFound')

        elif self.state is 'foundObject':
            self.subtask = self.subtaskBook.get_subtask('Grab')
            self.subtask.grab(self.objPos)
            self.change_state('grabObject')
            rospy.loginfo('grabObject')

        elif self.state is 'grabObject':
            if self.current_subtask.state is 'finish':
                # self.subtask = self.subtaskBook.get_subtask('BringObjectToPerson') # must make it
                # self.subtask.start(self.personName)
                self.change_state('bringObjectToPerson')
                rospy.loginfo('bringObjectToPerson')

        elif self.state is 'bringObjectToPerson':
            if self.current_subtask.state is 'finish':
                self.object = None
                self.personName = None
                self.change_state('finish')
                rospy.loginfo('Done')
            # Don't forget to add this subtask to subtask book

    def start(self, object, person):
        self.object = object
        self.personName = person
        self.change_state('start')
