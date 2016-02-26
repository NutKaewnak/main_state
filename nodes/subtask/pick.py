import rospy
from include.abstract_subtask import AbstractSubtask
from std_msgs.msg import Float64

__author__ = 'CinDy'


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.input_object_pos = None
        self.side_arm = 'right_arm'
        self.subtask = None
        self.check = None
        self.neck = None
        # self.pub_prismatic = rospy.Publisher('/dynamixel/prismatic_controller/command', Float64)

    def perform(self, perception_data):
        if self.state is 'init':
            # self.neck.tilt = -0.3
            # self.neck.pan = 0
            self.neck = self.skillBook.get_skill(self, 'TurnNeck')
            print '******init_subtask'
            self.neck.turn(-0.4, 0)
            self.change_state('setting_arm')

        elif self.state is 'setting_arm':
            self.skill = self.skillBook.get_skill(self, 'Pick')
            self.skill.pick_object(self.side_arm)
            print '*******current state in subtask = ' + self.state + '********'
            self.change_state('detect_object')

        # elif self.state is 'move_base':
        #     # print '***************wait_skill_for_open_gripper: in subtask********************'
        #     # print 'current state in subtask = ' + self.state +'********************'
        #     if self.skill.state is 'moving':
        #         rospy.loginfo('******moving:subtask******')
        #         # self.set_subtask_book()
        #         self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
        #         self.subtask.set_position(1, 0, 0)
        #         self.change_state('after_move')
        #
        # elif self.state is 'after_move':
        #     # rospy.loginfo('******after_move:subtask******')
        #     if self.subtask.state is 'finish':
        #         rospy.loginfo('******finish_move:subtask******')
        #         self.skill.after_mani()
        #         self.change_state('detect_object')
        #     elif self.subtask.state is 'move':
        #         rospy.loginfo('******move:move_relative*******')

        elif self.state is 'detect_object':
            # rospy.loginfo('******detect_object:subtask******')
            if self.skill.state is 'checking':
                rospy.loginfo('******checking:subtask******')
                self.check = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
                self.check.start()
                self.change_state('after_detect')

        elif self.state is 'after_detect':
            # rospy.loginfo('******after_detect:subtask******')
            if self.check.state == 'finish':
                # rospy.loginfo('******finish_detect:subtask******')
                if len(self.check.objects) > 0:
                    self.skill.set_object_pos(self.check.objects[0].point.x,
                                              self.check.objects[0].point.y,
                                              self.check.objects[0].point.z)
                    self.skill.after_mani()
                    self.change_state('grasp_object')

        elif self.state is 'grasp_object':
            print self.skill.state
            if self.skill.state is 'succeed':
                self.change_state('finish')
                #     self.change_state('receive_object')
                # elif self.state is 'receive_object':
                #     if self.skill.state is 'succeed':
                #         self.change_state('finish')

    def pick_object(self, side):
        rospy.loginfo('------in pick_object:subtask------')
        # self.input_object_pos = goal
        self.side_arm = side
        # self.pub_prismatic.publish(0+0.23)
        self.change_state('init')
