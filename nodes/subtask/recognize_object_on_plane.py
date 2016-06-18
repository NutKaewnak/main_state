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
        self.timer = Delay()
        self.neck_timer = Delay()
        self.report_generator = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.timer.wait(20)
            self.found_objects = []
            self.skillBook.get_skill(self, 'TurnNeck').turn(-0.1, 0)
            self.skill = self.skillBook.get_skill(self, 'RecognizeObjects')
            self.skill.recognize('*')
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if self.skill.state is 'succeeded':
                self.found_objects += self.skill.objects
                rospy.loginfo('Found: ' + str(self.found_objects) + ' object(s).')

                if self.report_generator:
                    for found_object in self.found_objects:
                        self.report_generator.generate_object_report(found_object)

                if len(self.found_objects) >= 4:
                    self.change_state('finish')

            elif not self.timer.is_waiting():
                self.change_state('time_out')

    def set_report_generator(self, report_generator):
        self.report_generator = report_generator
