__author__ = 'Nicole'
import rospy
import roslib
from include.abstract_task import AbstractTask
from include.delay import Delay


class ManipulationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.object_array = []
        self.number_object_found = 0
        self.pdf_file = None
        self.delay = Delay()
        self.latex = None
        self.is_make_latex = False

    def perform(self, perception_data):
        if self.state is 'init':
            # self.pdf_file = something
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectRecognition')  # this subtask is not created
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

            if self.delay.is_waiting() is False:
                self.change_state('run_out_of_time')

        elif self.state is 'run_out_of_time':
            self.on_end_latex()
            self.subtaskBook.get_subtask(self, 'Say').say('I\'m running out of time.')
            self.change_state('prepare_to_pick_object')

        elif self.state is 'prepare_to_pick_object':
            # self.subtask = self.subtaskBook.get_subtask(self, 'PickObject')
            self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.number_object_found is 0:
                self.change_state('finish')
            else:
                # self.subtask.pick(self.object_array[self.number_object_found])  # this subtask is not created
                rospy.loginfo('Picking ' + self.object_array[self.number_object_found])
                if self.subtask.state is 'finish':
                    self.number_object_found -= 1

    def to_pdf(self, object_to_pdf):
        if self.is_make_latex:
            self.make_tex_header()

        string_pic = 'object_description\n\\begin{figure}\n\\centering\n\\includegraphics[height=6.2cm]{' \
                     'object_picture_position}\n\\label{fig:base}\n\\end{figure}\n'

        # wait for object P'muk here NOT FINISH
        obj = string_pic.replace('object_description', object_to_pdf.time_stamp + '\n' + object_to_pdf.name)
        obj = obj.replace('object_picture_position', object_to_pdf.picture_directory)
        self.latex.write(obj + '\n\n')

    def make_tex_header(self):
        self.latex = open(roslib.packages.get_pkg_dir('main_state') + '/object.tex', 'rw')
        string_header = ['\documentclass[10pt,a4paper]{llncs}',
                         '\usepackage[latin1]{inputenc}'
                         '\usepackage{amsmath}'
                         '\usepackage{amsfonts}',
                         '\usepackage{amssymb}',
                         '\usepackage{graphicx}',
                         '',
                         '\\begin{document}',
                         '',
                         '\\title{SKUBA 2015 Object Recognition Report}',
                         '\\author{ }',
                         '\institute{ }',
                         '\maketitle', '']
        for line in string_header:
            self.latex.write(line + '\n')
        self.is_make_latex = True

    def on_end_latex(self):
        from subprocess import call

        self.latex.write('\end{document}')
        self.latex.close()
        call(['pdflatex', 'object.tex'])