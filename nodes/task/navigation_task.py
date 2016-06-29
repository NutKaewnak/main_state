import math
import rospy
import tf
import random
from geometry_msgs.msg import Point, Pose2D
# from include.location_information import read_location_information
from include.transform_point import transform_point
from std_srvs.srv import Empty
from include.abstract_task import AbstractTask
from include.delay import Delay
from include.get_distance import get_distance

__author__ = 'Nicole'


class NavigationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.delay = Delay()
        self.timer = Delay()
        self.follow = None
        self.is_people_blocked_waypoint_2 = False
        self.tf_listener = None
        self.waypoint_2 = Point()
        self.waypoint_2.x = 11.997
        self.waypoint_2.y = -6.004
        self.is_performing = False
        self.location_list = {}
        self.say = None
        self.obstrucle = None
        self.track_id = None
        # self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
        # self.subtask.static_pose('right_push_chair_push')

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        print self.state
        if self.state is 'init':
            rospy.loginfo('NavigationTask init')
            rospy.wait_for_service('/guess_detection/get')
            self.obstrucle = rospy.ServiceProxy('/guess_detection/get', Empty)
            self.tf_listener = tf.TransformListener()
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.3, 0)
            self.change_state('init_pass_door')

        elif self.state is 'init_pass_door':
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('move_pass_door')

        elif self.state is 'move_pass_door':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 2')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 2.')
                self.delay.wait(3)
                self.change_state('prepare_to_waypoint2')

        elif self.state is 'prepare_to_waypoint1':
            print 'prepare to waypoint 1'
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_1')
                self.delay.wait(90)
                self.timer.wait(10)
                self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            print 'going to waypoint1'
            if self.perception_module.base_status.position:
                print 'reset timer'
                self.timer.wait(10)
            elif not self.timer.is_waiting():
                print 'clear_costmap'
                self.subtask.clear_costmap()

            if self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('I reached waypoint 1.')
                self.delay.wait(2)
                self.change_state('prepare_to_waypoint3')
            elif not self.delay.is_waiting():
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 3.')
                self.delay.wait(2)
                self.change_state('prepare_to_waypoint3')
            elif self.subtask.state is 'error':
                rospy.loginfo('resend goal in waypoint_1')
                self.subtask.to_location('waypoint_1')

        elif self.state is 'prepare_to_waypoint2':
            if not self.delay.is_waiting():
                rospy.loginfo('going to waypoint 2')
                self.change_state('finding_obstacle_waypoint2')
                self.delay.wait(150)
                self.timer.wait(10)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('pre_waypoint_2')

        elif self.state is 'finding_obstacle_waypoint2':
            if self.perception_module.base_status.position:
                self.timer.wait(10)
            elif not self.timer.is_waiting():
                self.subtask.clear_costmap()

            if perception_data.device is 'PEOPLE' and perception_data.input is not []:
                print 'people' + str(perception_data.input)
                for x in perception_data.input:
                    print 'x =' + str(x)
                    point_tf = transform_point(self.tf_listener, x.personpoints, 'map')
                    if point_tf:
                        distance = get_distance(self.waypoint_2.x, point_tf)
                        print distance
                        if distance <= 2:
                            rospy.loginfo('Found people block the way')
                            self.is_people_blocked_waypoint_2 = True
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                obj = self.obstrucle()
                if self.is_people_blocked_waypoint_2:
                    self.change_state('blocked_by_people')
                elif obj == 'object':
                    self.change_state('blocked_by_object')
                elif obj == 'pet':
                    self.change_state('blocked_by_pet')
            elif self.subtask.state is 'error':
                # self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                # self.subtask.set_postion(0, 0, math.pi)
                self.subtask.to_location('pre_waypoint_2')
                self.timer.wait(10)
                # self.change_state('finding_obstacle_waypoint2')

        # elif self.state is 'move_back':
        #     if self.subtask.state is 'finish':
        #         self.subtask.set_postion(1.5, 0, math.pi)
        #         self.change_state('finding_obstacle_waypoint2')

        elif self.state is 'blocked_by_people':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('Excuse me. May I pass')
            self.delay.wait(5)
            self.change_state('enter_waypoint2')

        elif self.state is 'blocked_by_object':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('I found an object blocking my way.')
            self.change_state('push_object')

        elif self.state is 'push_object':
            self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            self.subtask.static_pose('right_push_chair_push')
            self.delay.wait(20)
            self.change_state('enter_waypoint2')
            self.is_performing = False

        elif self.state is 'blocked_by_pet':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtaskBook.say('I found a pet blocking my way.')
            self.delay.wait(30)
            self.change_state('enter_waypoiint2')

        elif self.state is 'enter_waypoint2':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.delay.wait(20)
                self.timer.wait(10)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_2')
                self.change_state('wait_enter_waypoint2')

        elif self.state is 'wait_enter_waypoint2':
            if self.perception_module.base_status.position:
                self.timer.wait(10)
            elif not self.timer.is_waiting():
                self.subtask.clear_costmap()

            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reached waypoint 2')
                self.change_state('prepare_to_waypoint1')
            elif not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I will go to waypoint 1')
                self.change_state('prepare_to_waypoint1')
            elif self.subtask.state is 'error':
                self.subtask.to_location('wayppoint_2')
                # self.change_state('wait_enter_waypoint2')

        elif self.state is 'prepare_to_waypoint3':
            if not self.delay.is_waiting():
                rospy.loginfo('prepare to waypoint 3')
                self.delay.wait(150)
                self.timer.wait(10)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_3')
                self.change_state('going_to_waypoint3')

        elif self.state is 'going_to_waypoint3':
            if self.perception_module.base_status.position:
                self.timer.wait(10)
            elif not self.timer.is_waiting():
                print 'clear_costmap'
                self.subtask.clear_costmap()

            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('please come in front of me and say \'follow me\'.')
                self.delay.wait(5)
                self.change_state('instruct')
            elif self.subtask.state is 'error':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_3')
                # self.change_state('going_to_waypoint3')

        elif self.state is 'instruct':
            if self.say.state is 'finish' or not self.delay.is_waiting():
                self.say.say('And \'robot go back\' to go back.')
                self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if perception_data.device is self.Devices.VOICE:
                if 'follow me' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'follow me\'? '
                                                                  'Please confirm by say \'robot yes\' or \'robot no\'.')
                    self.delay.wait(10)
                    self.change_state('confirm_follow')
                elif 'go back' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'go back\'? '
                                                                  'Please confirm by say \'robot yes\' or \'robot no\'.')
                    self.delay.wait(10)
                    self.change_state('confirm_back')

        elif self.state is 'confirm_follow':
            if perception_data.device is self.Devices.VOICE and not self.delay.is_waiting():
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                    self.change_state('follow_init')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('Sorry. Please tell me again.')
                    self.change_state('wait_for_command')

        elif self.state is 'confirm_back':
            if perception_data.device is self.Devices.VOICE and not self.delay.is_waiting():
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I will go back')
                    self.subtask = self.subtaskBook.get_subtask(self, 'DetectDoor')
                    self.change_state('prepare_back_to_waypoint_3')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('Sorry. Please tell me again.')
                    self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            # if perception_data.device is self.Devices.BASE_STATUS and self.perception_module.base_status.position:
            #     robo_position = self.perception_module.base_status.position
            #     # if math.sqrt(math.hypot(robo_position[0],robo_position[1]) ==
            #     self.door_waypoint3_path['x'].append(robo_position[0])
            #     self.door_waypoint3_path['y'].append(robo_position[1])
            #     self.door_waypoint3_path['theta'].append(robo_position[2])
            # if self.follow.state is 'abort':
            #     print 'abort'
            #     self.subtaskBook.get_subtask(self, 'Say').say('I will go back.')
            #     self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            #     self.delay.wait(5)
            #     # self.subtask.state = 'finish'
            #     self.change_state('prepare_back_to_waypoint_3')
            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input:
                min_distance = 99
                self.track_id = -1
                for person in perception_data.input.people:
                    if (person.pose.position.x > 0 and person.pose.position.x < 2
                        and person.pose.position.y > -1 and person.pose.position.y < 1):
                        distance = math.hypot(person.pose.position.x, person.pose.position.y)
                        if distance < min_distance:
                            self.track_id = person.id
                if self.track_id != -1:
                    print self.track_id.id
                    self.follow.set_person_id(self.track_id.id)
                    self.change_state('follow')

        elif self.state is 'follow':
            print 'state =' + self.state
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'stop' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                self.follow.set_person_id(-1)
                self.change_state('wait_for_command')

            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
                for person in perception_data.input.people:
                    if self.track_id == person.id:
                        break
                    elif self.follow.guess_id == person.id:
                        self.track_id = self.follow.guess_id
                        print 'change track id = ', self.track_id
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('I am lost tracking. Please wave your hand.')
                    self.delay.wait(2)
                    self.change_state('detect_waving_people')

        elif self.state is 'prepare_back_to_waypoint_3':
            # if self.subtask.state is 'finish' or self.subtask.state is 'error':
            # if not self.delay.is_waiting():
            #     print self.follow.goal_array
            #     if self.follow.goal_array:
            #         self.change_state('back_to_waypoint_3')
            #     else:
            #         self.subtaskBook.get_subtask(self, 'Say').say('I will leave arena.')
            #         self.change_state('prepare_leave_arena')
            if self.subtask.state is 'finish':
                print self.subtask.state
                self.delay.wait(150)
                self.timer.wait(10)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_3')
                self.change_state('back_to_waypoint_3')

        elif self.state is 'back_to_waypoint_3':
            # pose = self.follow.goal_array.pop()
            # self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            # self.subtask.set_position(pose.pose.position.x, pose.pose.position.y, math.pi-pose.pose.position.z)
            if self.perception_module.base_status.position:
                self.timer.wait(10)
            if not self.timer.is_waiting():
                self.subtask.clear_costmap()

            if self.subtask.state is 'finish':
                rospy.loginfo('leave arena')
                self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
                self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')

        self.is_performing = False