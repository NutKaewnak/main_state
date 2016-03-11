import rospy
from include.abstract_subtask import AbstractSubtask
from include.delay import Delay
__author__ = 'nicole'


class DetectWavingPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.gesture_pos = None
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            print 'detect_waving state = ' + self.state
            self.gesture_pos = None
            # self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            # self.skill.turn(-0.2, 0)
            # print 'pitch = '+str(self.skill.pitch)
            # print 'pan ='+str(self.skill.pan)
            self.change_state('searching')

        elif self.state is 'searching':
            # print 'hi'
            if not self.delay.is_waiting() or perception_data.device is self.Devices.GESTURE:
                print '--detecting--'
                if not perception_data.input:
                    self.change_state('not_found')
                else:
                    self.gesture_pos = perception_data.input
                    self.change_state('finish')
            else:
                # for i in xrange(20):
                #     print 'hello'
                self.change_state('not_found')

    def start(self):
        self.gesture_pos = None
        self.delay.wait(5)
        self.change_state('searching')

    def get_point(self):
        return self.gesture_pos
