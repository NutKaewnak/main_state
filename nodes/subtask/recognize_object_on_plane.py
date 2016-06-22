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
        self.delay = Delay()
        self.timer = Delay()
        self.neck_timer = Delay()
        self.report_generator = None
        self.debug_state = None

    def perform(self, perception_data):
        if self.delay.is_waiting():
            return

        if self.state != self.debug_state:
            self.debug_state = self.state
            print self.debug_state

        if self.state is 'init':
            self.timer.wait(20)
            self.skillBook.get_skill(self, 'TurnNeck').turn(-0.3, 0)
            self.skill = self.skillBook.get_skill(self, 'RecognizeObjects')
            self.skill.recognize(['*'])
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if self.skill.state is 'succeeded':
                self.delay.wait(2)

                for found_object in self.skill.object.result.objects:
                    if found_object.name.data not in self.found_objects_name:
                        self.found_objects_name.append(found_object.name.data)
                        self.found_objects.append(found_object)

                rospy.loginfo('Found: ' + str(len(self.skill.object.result.objects)) + ' object(s).')

                if self.report_generator:
                    print 'generate', len(self.found_objects), 'object(s)'
                    for found_object in self.found_objects:
                        self.report_generator.generate_object_report(found_object)
                    self.report_generator = None

                print 'found_object_name', self.found_objects_name
                self.change_state('finish')

            elif not self.timer.is_waiting():
                self.change_state('time_out')

    def set_report_generator(self, report_generator):
        self.report_generator = report_generator
