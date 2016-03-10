import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class VoiceRecognitionMode(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'VoiceRecognitionMode')
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'active':
            if self.skill.state is 'succeed':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                rospy.loginfo('Aborted at MovePassDoor')
                self.change_state('error')

    def recognize(self, voice_id):
        self.change_state('active')
        self.skill.recognize(voice_id)
