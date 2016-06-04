from include.abstract_task import AbstractTask
from math import hypot

__author__ = 'Frank Tower'


class TestFollowLeg(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        # print self.state
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                self.change_state('follow_init')

        elif self.state is 'follow_init' and perception_data.device is self.Devices.PEOPLE_LEG:
            # print 1111
            min_distance = 99
            track_id = -1
            for person in perception_data.input.people:
                if (person.pose.position.x > 0 and person.pose.position.x < 2
                    and person.pose.position.y > -1 and person.pose.position.y < 1):
                    distance = hypot(person.pose.position.x, person.pose.position.y)
                    if distance < min_distance:
                        track_id = person.id
            if track_id != -1:
                print person.id
                self.follow.set_person_id(person.id)
                self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'stop' in perception_data.input:
                self.change_state('init')
