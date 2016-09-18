from include.abstract_task import AbstractTask
from math import hypot
from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import *

__author__ = 'Frank Tower'


class TestFollowLeg(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        print self.state
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.marker_pub = rospy.Publisher("/visualization_marker", Marker)
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            box_marker = Marker()

            box_marker.header.frame_id = "/base_link"

            box_marker.type = Marker.CUBE
            box_marker.scale.x = 1
            box_marker.scale.y = 1
            box_marker.scale.z = 0.7
            box_marker.color.r = 0.0
            box_marker.color.g = 0.5
            box_marker.color.b = 0.5
            box_marker.color.a = 0.2

            box_marker.pose.position.x = 1.0/2 + 0.8
            box_marker.pose.position.y = 0
            box_marker.pose.position.z = 0.7/2

            self.marker_pub.publish(box_marker)
            print "----"
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                # self.server.clear()
                self.change_state('follow_init')

        elif self.state is 'follow_init' and perception_data.device is self.Devices.PEOPLE_LEG:
            min_distance = 99
            track_id = -1
            print perception_data.input.people
            for person in perception_data.input.people:
                if (person.pos.x > 0.2 and person.pos.x < 1.2
                    and person.pos.y > -0.5 and person.pos.y < 0.5):
                    distance = hypot(person.pos.x, person.pos.y)
                    if distance < min_distance:
                        track_id = person.object_id
            if track_id != -1:
                print track_id
                self.follow.set_person_id(track_id)
                self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'stop' in perception_data.input:
                self.change_state('init')
