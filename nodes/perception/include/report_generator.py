#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import String, Header
from geometry_msgs.msg import PointStamped, Point, Pose2D
from sensor_msgs.msg import Image
from object_3d_detector.msg import Object3DsResult, Object3D
from object_recognition_v2.msg import ObjectRecognition, ObjectRecognitions
from subprocess import call
from devices import Devices


class ReportGenerator:
    def __init__(self, task_name='Manipulator'):
        self.filename = '/SKUBA_'
        self.header = ['\documentclass[10pt,a4paper]{article}',
                       '\usepackage[latin1]{inputenc}',
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
        self.filename += task_name + '.tex'
        self.header += [task_name, '']
        self.open_latex()

    def open_latex(self):
        self.latex = open(roslib.packages.get_pkg_dir('main_state') + self.filename, 'wr')

    def make_tex_header(self):
        self.open_latex()
        for line in self.header:
            self.latex.write(line + '\n')
        self.is_make_latex = True

    def generate_object_report(self, data):
        """

        :param data: (ObjectRecognition)
        :return:
        """
        pic_description = 'data_description\n\\begin{figure}\n\\centering\n\\includegraphics[height=5cm]{' \
                          'data_picture}\n\\label{fig:base}\n\\end{figure}\n'
        info_to_write = pic_description.replace('data_description', 'Time Stamped: ' + str(data.header.stamp.to_time())
                                                + '\n' + 'Centroid: \n' + str(data.centriod)
                                                + '\n' + 'Name: ' + data.name.data)
        info_to_write = info_to_write.replace('data_picture', roslib.packages.get_pkg_dir('main_state') + '/picture/rock.jpg')
        self.latex.write(info_to_write)

    def on_end_latex(self):
        self.latex.write('\end{document}')
        self.latex.close()
        call(['pdflatex', '-output-directory=' + roslib.packages.get_pkg_dir('main_state'),
              roslib.packages.get_pkg_dir('main_state') + self.filename])


if __name__ == "__main__":
    rospy.init_node('test_report_gen')

    example_data = ObjectRecognition()
    example_data.header = Header()
    example_data.header.stamp = rospy.Time.now()
    example_data.centriod = Pose2D()
    example_data.point = Point()
    example_data.image = Image()
    example_data.name = String('test na ja')

    report = ReportGenerator()
    report.generate_object_report(example_data)
    report.on_end_latex()
