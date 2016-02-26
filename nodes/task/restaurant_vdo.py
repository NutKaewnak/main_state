import rospy
from include.abstract_task import AbstractTask
from include.get_distance import get_distance
from include.delay import Delay
from std_msgs.msg import Float64

__author__ = 'Nicole'


class RestaurantVDO(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.init_location = None
        self.location_list = {'location one': [], 'location two': [], 'location three': []}
        self.command = None
        self.count = 0
        self.first = None
        self.say = None
        self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
        self.arm_init()
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.PEOPLE:
                distance = 3.0  # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if self.say.state is not 'finish':
                return
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 2  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = get_distance(person.personpoints, self.follow.last_point)
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE:
                if 'robot stop' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Where is this place ?')
                    self.change_state('ask_for_location')
                elif 'robot waiting' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Wait for command.')
                    self.change_state('wait_for_command')

        elif self.state is 'ask_for_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('This is ' + location + ' yes or no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                print self.location_list
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'wait_for_command':
            if self.say.state is not 'init' and self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                print perception_data.input
                print self.location_list
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('bring cup noodle to ' + self.command + ' yes or no ?')
                        self.change_state('confirm_command')

                if 'follow me' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('I will follow you.')
                    self.change_state('follow_init')
                elif 'get out' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('I will go back.')
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.move = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                    self.move.to_location('gpsr_start')
                    self.change_state('move_to_gpsr_start')

        elif self.state is 'confirm_command':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.mama()
                self.pub_left_gripper.publish(1.1)
                rospy.sleep(5)
                self.pub_left_gripper.publish(-0.4)
                rospy.sleep(3)
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I will go to ' + self.command + '.')
                self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move.set_position(self.location_list[self.command][0], self.location_list[self.command][1], self.location_list[self.command][2])
                self.change_state('move_to_first')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_command')

        elif self.state is 'move_to_first':
            if self.move.state is 'finish':
                self.change_state('wait_for_order')

        elif self.state is 'wait_for_order':
            if perception_data.device is self.Devices.VOICE:
                self.send()
                self.pub_left_gripper.publish(1.1)
                # self.say.say('you want ' + perception_data.input + ' yes or no ?')
                # for location in self.location_list:
                #     if location in perception_data.input:
                #         self.command = location
                #         self.say.say('go to ' + self.command + ' yes or no ?')
                #         self.change_state('confirm_command')

        elif self.state is 'move_to_gpsr_start':
            if self.current_subtask.state is 'finish':
                self.change_state('wait_for_command')

    def arm_init(self):
        self.pub_left_shoulder_1 = rospy.Publisher('/dynamixel/left_shoulder_1_controller/command', Float64)
        self.pub_left_shoulder_2 = rospy.Publisher('/dynamixel/left_shoulder_2_controller/command', Float64)
        self.pub_left_elbow = rospy.Publisher('/dynamixel/left_elbow_controller/command', Float64)
        self.pub_left_wrist_1 = rospy.Publisher('/dynamixel/left_wrist_1_controller/command', Float64)
        self.pub_left_wrist_2 = rospy.Publisher('/dynamixel/left_wrist_2_controller/command', Float64)
        self.pub_left_wrist_3 = rospy.Publisher('/dynamixel/left_wrist_3_controller/command', Float64)
        self.pub_left_gripper = rospy.Publisher('dynamixel/left_gripper_joint_controller/command', Float64)

    def mama(self):
        self.pub_left_shoulder_2.publish(0.2)
        self.pub_left_elbow.publish(0.4)
        self.pub_left_wrist_1.publish(0.0)
        self.pub_left_wrist_2.publish(0.4)
        self.pub_left_wrist_3.publish(0.0)
        self.pub_left_shoulder_1.publish(-0.1)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.2)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.3)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.4)
        rospy.sleep(0.5)

    def send(self):
        self.pub_left_shoulder_2.publish(0.2)
        self.pub_left_elbow.publish(0.2)
        self.pub_left_wrist_1.publish(0.0)
        self.pub_left_wrist_2.publish(0.8)
        self.pub_left_wrist_3.publish(0.0)
        self.pub_left_shoulder_1.publish(-0.5)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.6)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.7)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.8)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-0.9)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.0)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.1)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.2)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.3)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.4)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.5)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.6)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.7)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.8)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-1.9)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-2.0)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-2.1)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-2.2)
        rospy.sleep(0.5)
        self.pub_left_shoulder_1.publish(-2.3)
        rospy.sleep(0.5)

