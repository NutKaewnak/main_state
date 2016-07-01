from math import hypot, atan, sin, cos, pi
from include.abstract_task import AbstractTask
from include.delay import Delay
from geometry_msgs.msg import Pose2D

__author__ = 'CinDy'


class FollowGuiding(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.follow = None
        self.timer = Delay()
        self.track_id = None
        self.path = []
        self.move = None

    def perform(self, perception_data):
        # print 'state = ' + self.state
        if self.state is 'init':
            # self.path['x'] = []
            # self.path['y'] = []
            # self.path['theta'] = []

            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            # self.change_state('training_phase')
            self.change_state('wait_for_command')

        elif self.state is 'training_phase':
            if perception_data.device is self.Devices.VOICE and perception_data.input == 'robot start':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('please come in front of me and say \'follow me\'. '
                                 '\'robot stop\' to stop. and \'guide back\' to guide back')
                self.timer.wait(10)
                self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            # print 'subtask state ='+self.subtask.state
            # print 'state =' + self.state
            # if self.subtask.state is 'finish' or not self.timer.is_waiting():
            if perception_data.device is self.Devices.VOICE:
                print 'input = ' + str(perception_data.input)
                if perception_data.input == 'follow me':
                    self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'follow me\'? '
                                                                  'Please confirm by say \'robot yes\' or \'robot no\'.')
                    self.timer.wait(10)
                    self.change_state('confirm_follow')
                elif perception_data.input == 'guide back':
                    self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'guide back\'? '
                                                                  'Please confirm by say \'robot yes\' or \'robot no\'.')
                    self.timer.wait(10)
                    self.change_state('confirm_guide')
                    
        elif self.state is 'confirm_follow':
            if perception_data.device is self.Devices.VOICE:
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                    self.change_state('follow_init')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('Sorry. Please tell me again.')
                    self.change_state('wait_for_command')
                    
        elif self.state is 'confirm_guide':
            if perception_data.device is self.Devices.VOICE:
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I will guide you back')
                    self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                    self.change_state('init_guide')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('Sorry. Please tell me again.')
                    self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            # print 'state =' + self.state
            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input:
                min_distance = 99
                self.track_id = -1
                for person in perception_data.input.people:
                    print 'person = ', person
                    if (person.pos.x > 0.8 and person.pos.x < 1.8
                        and person.pos.y > -1 and person.pos.y < 1):
                        distance = hypot(person.pos.x, person.pos.y)
                        print 'person id =', person.object_id
                        if distance < min_distance:
                            self.track_id = person.object_id
                if self.track_id != -1:
                    print self.track_id
                    self.follow.set_person_id(self.track_id)
                    self.change_state('follow')

        elif self.state is 'follow':
            print 'state =' + self.state
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'robot stop\'? '
                                                              'Please confirm by say \'robot yes\' or \'robot no\'.')
                # self.follow.set_person_id(-1)
                self.change_state('comfirm_stop')

            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
                print 'track_id =', self.track_id
                for person in perception_data.input.people:
                    print ' person.id =', person.id
                    if self.track_id == person.id:
                        break
                    elif self.follow.guess_id == person.id:
                        self.track_id = self.follow.guess_id
                        print 'change track id = ', self.track_id
                    # elif perception_data.input.people[-1]:
                    elif self.follow.isLost: 
                        self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                        self.subtask.say('I am lost tracking. Please wave your hand.')
                        self.timer.wait(2)
                        self.change_state('detect_waving_people')
            # if perception_data.device is self.Devices.BASE_STATUS and self.perception_module.base_status.position:
            #     robot_position = self.perception_module.base_status.position
            #     pos = Pose2D()
            #     pos.x = robot_position[0]
            #     pos.y = robot_position[1]
            #     pos.theta = robot_position[2]
            #     self.path.append(pos)
                # self.path['x'].append(robot_position[0])
                # self.path['y'].append(robot_position[1])
                # self.path['theta'].append(robot_position[2])
            if perception_data.device is self.Devices.NAVIGATE and perception_data.input:
                print perception_data.input

        elif self.state is 'detect_waving_people':
            if self.subtask.state is 'finish' and not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
                self.change_state('searching_person')

        elif self.state is 'searching_person':
            if self.subtask.state is 'finish':
                person_pos = self.subtask.waving_people_point
                theta = atan(person_pos.point.y / person_pos.point.x)
                print "person pos = " + str(person_pos)
                # person_theta = atan(person_pos.point.x / person_pos.point.y)
                # person_pos.point.x = person_pos.point.x * sin(person_theta)
                # person_pos.point.y = person_pos.point.y * cos(person_theta)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_position(person_pos.point.x - 0.5, person_pos.point.y,
                                          theta)
                self.change_state('move_to_person')

        elif self.state is 'move_to_person':
            if perception_data.device is 'BASE_STATUS' and perception_data.input == 3:
                self.change_state('wait_for_command')

        elif self.state is 'confirm_stop':
            if perception_data.device is self.Devices.VOICE and not self.delay.is_waiting():
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I stop.')
                    self.follow.set_person_id(-1)
                    self.change_state('wait_for_command')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('continue following')
                    self.change_state('follow')

        elif self.state is 'init_guide':
            point = Pose2D()
            point = self.follow.path.pop()
            print 'point = ',point
            self.move.set_position(point.x, point.y, (point.theta+pi) % (2*pi))
            self.change_state('guide_back')

        elif self.state is 'guide_back':
            if self.move.state is 'finish':
                self.change_state('init_guide')
