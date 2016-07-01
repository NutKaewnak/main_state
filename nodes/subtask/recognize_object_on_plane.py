import rospy
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask

__author__ = 'Nicole'


class RecognizeObjectOnPlane(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.found_objects = []
        self.found_objects_name = []
        self.timer = Delay()
        self.neck_timer = Delay()
        self.report_generator = None
        self.debug_state = None

    def perform(self, perception_data):
        if self.state != self.debug_state:
            self.debug_state = self.state
            print self.debug_state

        if self.state is 'init':
            self.timer.wait(20)
            self.skillBook.get_skill(self, 'TurnNeck').turn(-0.35, 0)
            self.skill = self.skillBook.get_skill(self, 'RecognizeObjects')
            self.skill.recognize(['*'])
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if self.skill.state is 'succeeded':
                for found_object in self.skill.object.result.objects:
                    if found_object.name.data not in self.found_objects_name:
                        self.found_objects_name.append(found_object.name.data)
                        self.found_objects.append(found_object)
                    else:
                        for x in xrange(len(self.found_objects)):
                            if found_object.name.data == self.found_objects[x].name.data:
                                if found_object.confident > self.found_objects[x].confident:
                                    self.found_objects.pop(x)
                                    self.found_objects.append(found_object)

                rospy.loginfo('Found: ' + str(len(self.skill.object.result.objects)) + ' object(s).')

                self.change_state('finish')

            elif not self.timer.is_waiting():
                self.change_state('time_out')
