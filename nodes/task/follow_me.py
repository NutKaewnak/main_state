from include.abstract_task import AbstractTask
from math import hypot
__author__ = 'AThousandYears'


class FollowMe(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                # self.server.clear()
                self.change_state('follow_init')

        elif self.state is 'follow_init' and perception_data.device is self.Devices.PEOPLE_LEG:
            min_distance = 99
            track_id = -1
            print perception_data.input.people
            for person in perception_data.input.people:
                if (person.pos.x > 0.8 and person.pos.x < 1.8
                    and person.pos.y > -1 and person.pos.y < 1):
                    distance = hypot(person.pos.x, person.pos.y)
                    if distance < min_distance:
                        track_id = person.object_id
            if track_id != -1:
                print track_id
                self.follow.set_person_id(track_id)
                self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'stop' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I stopped.')
                self.change_state('init')
