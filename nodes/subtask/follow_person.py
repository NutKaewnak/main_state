import rospy
import tf
from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist, Vector3, PoseStamped, Pose2D, PointStamped
from tf.transformations import quaternion_from_euler
from include.transform_point import transform_point

__author__ = 'AThousandYears'


class FollowPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.move = None
        self.turn_base = None
        self.turn_neck = None
        self.set_tilt = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        self.set_pan = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        self.last_point = Vector3()
        self.person_id = None
        self.distance_from_last = 9999.0
        self.offset_from_person = 0.3
        self.goal_array = []
        self.tf_listener = tf.TransformListener()

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
            self.turn_base = rospy.Publisher('/base/cmd_vel', Twist)
            self.publish_goal = rospy.Publisher('/people/goal', PoseStamped)
            self.change_state('wait')

        elif self.state is 'follow' and perception_data.device is self.Devices.PEOPLE:
            rospy.loginfo("Track Person id %d", self.person_id)
            point = None
            for person in perception_data.input:
                if person.id == self.person_id:
                    point = person.personpoints.point

            if point is not None:
                theta = atan(point.y/point.x)
                print 'theta'
                print theta
                self.set_pan.publish(theta)
                self.set_tilt.publish(-0.1)

                size = sqrt(point.x**2 + point.y**2)

                x = max(point.x/size*(size*0.5), 0)
                y = point.y/size*(size*0.5)

                publish_pose = PoseStamped()
                # publish_pose = PointStamped()
                publish_pose.header.stamp = rospy.Time.now()
                publish_pose.header.frame_id = 'base_link'

                publish_pose.pose.position.x = x
                publish_pose.pose.position.y = y

                quaternion = quaternion_from_euler(0, 0, theta)
                publish_pose.pose.orientation.z = quaternion[2]
                publish_pose.pose.orientation.w = quaternion[3]
                self.publish_goal.publish(publish_pose)
                
                self.move.set_position(x, y, theta)
                pose = self.perception_module.base_status.position

                # TODO: erase this debug code when done
                print 'follow person pose'
                print pose
                input_pts = PointStamped()
                input_pts.header.stamp = rospy.Time(0)
                input_pts.header.frame_id = 'base_link'
                input_pts.point.x = x
                input_pts.point.y = y
                input_pts.point.z = 0

                #temp = transform_point(self.tf_listener, input_pts, '/map')
                #print 'follow person temp'
                #print temp
                # convert back to pose
                #out = PoseStamped()
                #out.header.stamp = rospy.Time.now()
                #out.header.frame_id = '/map'
                #out.pose.position.x = temp.x
                #out.pose.position.y = temp.y
                #out.pose.position.z = theta
                # theta2 = atan(temp.point.y/temp.point.x)
                # quaternion = quaternion_from_euler(0, 0, theta2)
                # HACKING find pose of person
                # out.pose.orientation.z = quaternion[2]
                # out.pose.orientation.w = quaternion[3]

                # out.pose.position.x = temp.point.x
                # pose = temp

                self.goal_array.append([0,0,0])

                self.distance_from_last = sqrt((point.x - self.last_point.x) ** 2 + (point.y - self.last_point.y) ** 2)

                self.last_point = point

            else:
                rospy.loginfo("Stop Robot")
                # self.skillBook.get_skill(self, 'Say').say('I cannot find you. Please come in front of me.')
                # self.turn_neck.turn(0, 0)
                self.move.stop()
                self.change_state('abort')

        elif perception_data.device is self.Devices.VOICE:
            if perception_data.input == 'stop':
                self.skillBook.get_skill(self, 'Say').say('I stop.')
                self.move.stop()
                self.change_state('abort')
