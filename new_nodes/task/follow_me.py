__author__ = 'AThousandYears'
import rospy
from include.abstract_task import AbstractTask


class FollowMe(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
                self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                distance = 9999.0 # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
                    self.change_state('follow')
        elif self.state is 'follow':
            pass
