import rospy
import tf
import random
from geometry_msgs.msg import Point, Pose2D
# from include.location_information import read_location_information
from include.transform_point import transform_point
from std_srvs.srv import Empty
from include.abstract_task import AbstractTask
from include.delay import Delay
from math import hypot

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
        self.waypoint_2.x = 6.862
        self.waypoint_2.y = -8.177
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
            # rospy.wait_for_service('/guess_detection/get')
            # self.obstrucle = rospy.ServiceProxy('/guess_detection/get', Empty)
            self.tf_listener = tf.TransformListener()
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
            self.change_state('init_pass_door')
            # self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
            # self.change_state('prepare_to_waypoint1')

        elif self.state is 'init_pass_door':
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('move_pass_door')

        elif self.state is 'move_pass_door':
            if self.current_subtask.state is 'finish':
                # rospy.loginfo('going to waypoint 2')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 2.')
                self.delay.wait(4)
                self.change_state('prepare_to_waypoint2')

        elif self.state is 'prepare_to_waypoint2':
            if not self.delay.is_waiting():
                rospy.loginfo('going to waypoint 2')
                self.delay.wait(43)
                self.timer.wait(10)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('pre_waypoint_2')
                self.change_state('finding_obstacle_waypoint2')

        elif self.state is 'finding_obstacle_waypoint2':
            if self.perception_module.base_status.position:
                print 'move'
                self.timer.wait(10)
            elif not self.timer.is_waiting():
                print 'clear_costmap'
                self.subtask.clear_costmap()
                self.timer.wait(10)

            if perception_data.device is 'PEOPLE' and perception_data.input is not []:
                print 'people' + str(perception_data.input)
                for person in perception_data.input:
                    point_tf = transform_point(self.tf_listener, person.personpoints, 'map')
                    print 'point_tf =', point_tf
                    print 'person =' + str(person)
                    if point_tf:
                        distance = hypot((self.waypoint_2.x - point_tf.x), (self.waypoint_2.y - point_tf.y))
                        print distance
                        if distance <= 2:
                            rospy.loginfo('Found people block the way')
                            self.is_people_blocked_waypoint_2 = True

            if self.subtask.state is 'finish' or self.is_people_blocked_waypoint_2:
                print 'detect obstacle'
                # obj = self.obstrucle()
                if self.is_people_blocked_waypoint_2:
                    self.change_state('blocked_by_people')
                else:
                # elif obj == 'object':
                    self.change_state('blocked_by_object')
                # elif obj == 'pet':
                #     self.change_state('blocked_by_pet')
            elif self.subtask.state is 'error' or not self.delay.is_waiting():
                # self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                # self.subtask.set_postion(0, 0, math.pi)
                self.subtaskBook.get_subtask(self, 'Say').say('I can\'t go to waypoint 2. I will go to waypoint 1.')
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_1')
                self.timer.wait(10)
                self.change_state('going_to_waypoint1')

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
            # self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            # self.subtask.static_pose('right_push_chair_push')
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
            # if self.perception_module.base_status.position:
            #     self.timer.wait(10)
            # elif not self.timer.is_waiting():
            #     self.subtask.clear_costmap()
            #     self.timer.wait(10)

            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reached waypoint 2')
                self.change_state('prepare_to_waypoint1')
            elif not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I will go to waypoint 1')
                self.change_state('prepare_to_waypoint1')
            elif self.subtask.state is 'error':
                self.subtask.to_location('waypoint_2')
                # self.change_state('wait_enter_waypoint2')

        elif self.state is 'prepare_to_waypoint1':
            print 'prepare to waypoint 1'
            # if self.subtask.state is 'finish':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_1')
            self.delay.wait(94)
            self.timer.wait(10)
            self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            print 'going to waypoint1'
            # if self.perception_module.base_status.position:
            #     print 'reset timer'
            #     self.timer.wait(10)
            # elif not self.timer.is_waiting():
            #     print 'clear_costmap'
            #     self.subtask.clear_costmap()
            #     self.timer.wait(10)

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

        elif self.state is 'prepare_to_waypoint3':
            if not self.delay.is_waiting():
                rospy.loginfo('prepare to waypoint 3')
                self.delay.wait(60)
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
                self.timer.wait(10)

            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('please come in front of me and say \'follow me\' \'robot stop\' to stop.')
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
                    print 'person = ', person
                    if (person.pos.x > 0.8 and person.pos.x < 1.8
                        and person.pos.y > -1 and person.pos.y < 1):
                        distance = hypot(person.pos.x, person.pos.y)
                        print 'person id =', person.object_id
                        if distance < min_distance:
                            self.track_id = person.object_id
                if self.track_id != -1:
                    print self.track_id
                    self.follow.set_person_id(self.track_id)
                    self.change_state('follow')

        elif self.state is 'follow':
            print 'state =' + self.state
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('Did you say \'robot stop\'? '
                                                              'Please confirm by say \'robot yes\' or \'robot no\'.')
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                self.change_state('comfirm_stop')

            # if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
            #     for person in perception_data.input.people:
            #         if self.track_id == person.object_id:
            #             break
                    # elif self.follow.guess_id == person.object_id:
                    #     self.track_id = self.follow.guess_id
                    #     print 'change track id = ', self.track_id
            if self.follow.isLost:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I am lost tracking. Please wave your hand.')
                self.delay.wait(2)
                self.change_state('detect_waving_people')

        elif self.state is 'confirm_stop':
            if perception_data.device is self.Devices.VOICE and not self.delay.is_waiting():
                if perception_data.input == 'robot yes':
                    self.subtaskBook.get_subtask(self, 'Say').say('I stop.')
                    self.follow.set_person_id(-1)
                    self.change_state('wait_for_command')
                elif perception_data.input == 'robot no':
                    self.subtaskBook.get_subtask(self, 'Say').say('continue following')
                    self.change_state('follow')

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
                self.delay.wait(60)
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
                self.timer.wait(10)

            if self.subtask.state is 'finish':
                rospy.loginfo('leave arena')
                self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
                self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')

        elif self.state is 'detect_waving_people':
            if self.subtask.state is 'finish' and not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
                self.change_state('searching_person')

        elif self.state is 'searching_person':
            if self.subtask.state is 'finish':
                person_pos = self.subtask.waving_people_point
                theta = atan(person_pos.point.y / person_pos.point.x)
                print "person pos = " + str(person_pos)
                # person_theta = atan(person_pos.point.x / person_pos.point.y)
                # person_pos.point.x = person_pos.point.x * sin(person_theta)
                # person_pos.point.y = person_pos.point.y * cos(person_theta)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_position(person_pos.point.x - 0.5, person_pos.point.y,
                                          theta)
                self.change_state('move_to_person')

        elif self.state is 'move_to_person':
            if perception_data.device is 'BASE_STATUS' and perception_data.input == 3:
                self.subtaskBook.get_subtask(self, 'Say').say('waiting for command')
                self.change_state('wait_for_command')

        self.is_performing = False