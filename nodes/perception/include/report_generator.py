#!/usr/bin/env python
import rospy
import roslib
from pyPdf import PdfFileWriter, PdfFileReader
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import Image
from object_recognition_v2.msg import RecognizeObjectsFeedback, RecognizeObjectsResult
from subprocess import call

from devices import Devices


class ReportGenerator:
    def __init__(self, task_name='Manipulator'):
        self.filename = 'SKUBA_'
        self.header = ['\documentclass[10pt,a4paper]{llncs}',
                         '\usepackage[latin1]{inputenc}',
                         '\usepackage{amsmath}',
                         '\usepackage{amsfonts}',
                         '\usepackage{amssymb}',
                         '\usepackage{graphicx}',
                         '',
                         '\\begin{document}',
                         '',
                         '\\title{SKUBA 2016 Task Report}',
                         '\\author{ }',
                         '\institute{ }',
                         '\maketitle', '']
        self.latex = None
        self.set_task_name(task_name)
        self.is_make_latex = False
        self.make_tex_header()

    def set_task_name(self, task_name):
        self.filename += '/' + task_name + '.tex'
        self.header += task_name
        self.open_latex()

    def open_latex(self):
        self.latex = open(roslib.packages.get_pkg_dir('main_state') + self.filename, 'rw')

    def make_tex_header(self):
        self.open_latex()
        for line in self.header:
            self.latex.write(line + '\n')
        self.is_make_latex = True

    def generate_object_report(self, data):
        """

        :param data: (RecognizeObjectsResult)
        :return:
        """
        RecognizeObjectsResult(data)
        pic_description = 'data_description\n\\begin{figure}\n\\centering\n\\includegraphics[height=6.2cm]{' \
                     'data_picture}\n\\label{fig:base}\n\\end{figure}\n'
        info_to_write = pic_description.replace('data_description', data.header.time + data.centriod + '\n' + data.name)
        info_to_write = info_to_write.replace('data_picture', data.picture_directory)
        self.latex.write(info_to_write)

    def on_end_latex(self):
        self.latex.write('\end{document}')
        self.latex.close()
        call(['pdflatex', self.filename])


if __name__ == "__main__":
    report = ReportGenerator()
    report.generate_object_report(RecognizeObjectsResult())
