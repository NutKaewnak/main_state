__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay


class ManipulationTask(AbstractTask):
    # need reportlab to run this task
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.object_array = []
        self.number_object_found = 0
        self.pdf_file = None
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            # self.pdf_file = something
            self.subtask = self.subtaskBook.get_subtask(self, 'Recognition')
            self.delay.wait(90)
            self.change_state('recognition_object_on_shelf')

        elif self.state is 'recognition_object_on_shelf':
            if self.subtask.isFound():
                # make subtask find object first
                found_object = self.subtask.get_object()
                self.object_array.append(found_object)

                # add data to pdf here
                self.to_pdf(self.subtask.get_object())

                self.number_object_found += 1
                rospy.loginfo('Found: '+self.number_object_found+' '+object)

            if self.subtask.state is 'finish':
                if self.number_object_found == 5:
                    self.change_state('prepare_to_pick_object')
                else:
                    self.subtask.refind()

            if self.delay.is_waiting() is False :
                self.change_state('run_out_of_time')

        elif self.state is 'run_out_of_time':
            self.subtaskBook.get_subtask('Say').say('I\'m running out of time.')
            self.change_state('prepare_to_pick_object')

        elif self.state is 'prepare_to_pick_object':
            self.subtask = self.subtaskBook.get_subtask(self, 'PickObject')
            self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.number_object_found is 0:
                self.change_state('finish')
            else:
                self.subtask.pick(self.object_array[self.number_object_found])
                rospy.loginfo('Picking ' + self.object_array[self.number_object_found])
                if self.subtask.state is 'finish':
                    self.number_object_found -= 1

            # Don't forget to create launch file
    def to_pdf(self, object):
        # wait for object P'muk here NOT FINISH
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        image = object.get_picture()
        c = canvas.Canvas(self.number_object_found + '.pdf')
        c.drawImage(image, 40, 300, 38.46/2*cm, 24.12/2*cm)
        c.drawString(10*cm, 15*cm, 'something')
        c.showPage()
        c.save()