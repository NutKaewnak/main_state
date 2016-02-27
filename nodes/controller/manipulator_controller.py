import rospy
import moveit_commander
import moveit_msgs.msg
import trajectory_msgs.msg
import tf
import sys
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Point
from geometry_msgs.msg import PointStamped

__author__ = "ftprainnie"

GRIPPER_FRAME = 'right_wrist_3_Link'
GRIPPER_JOINT_NAMES = ['right_gripper_joint']

GRIPPER_OPENED = 0.1
GRIPPER_CLOSED = -0.5
GRIPPER_NEUTRAL = 0.0
GRASP_OVERTIGHTEN = -0.01
GRIPPER_EFFORT = 0.2
URDF_ELBOW_LIMIT = 0.2
URDF_WRIST2_LIMIT = -0.40

GRIPPER_PITCH_OFFSET = 0.2
EEF_OFFSET = []

REFERENCE_FRAME = 'base_link'


class ManipulateController:
    def __init__(self):
        # group should be "left_arm" or "right_arm
        self.pick_state = {"object_name": None,
                           "arm_group": None,
                           "object_position": None,
                           "ref_frame": None}
        self.set_torque_limit = {}
        self.GRIPPER_OPENED = 0.0
        self.GRIPPER_CLOSED = -0.8
        self.pregrasp_distance = 0
        self.pregrasp_value = Pose2D()
        self.object_position = Point()
        self.grasp_plan = None
        self.robot = None
        self.scene = None
        self.right_arm_group = None
        self.right_gripper_group = None
        self.left_arm_group = None
        self.left_gripper_group = None
        self.tf_listener = None

    def init_controller(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.tf_listener = tf.TransformListener()
        print 'kuy'
        self.right_arm_group = moveit_commander.MoveGroupCommander('right_arm')
        print dir(self.right_arm_group.clear_pose_targets)
        self.right_gripper_group = moveit_commander.MoveGroupCommander('right_gripper')
        self.left_arm_group = moveit_commander.MoveGroupCommander('left_arm')
        self.left_gripper_group = moveit_commander.MoveGroupCommander('left_gripper')

    def transform_point(self, position, arm_group, origin_frame='base_link'):
        destination_frame = None
        if arm_group == "right_arm":
            destination_frame = 'right_mani_link'
        elif arm_group == "left_arm":
            destination_frame = 'left_mani_link'

        tf_points = PointStamped()
        tf_points.point.x = position[0]
        tf_points.point.y = position[1]
        tf_points.point.z = position[2]
        tf_points.header.stamp = rospy.Time(0)
        tf_points.header.frame_id = origin_frame
        point_out = self.tf_listener.transform_point(destination_frame, tf_points)
        return point_out.point

    def manipulate(self, arm_group, position, orientation_rpy=[0, 0, 0], tolerance=[0.05, 0.1], ref_frame="base_link",
                   planning_time=50.00):

        pose_target = Pose()
        quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0],
                                                              orientation_rpy[1],
                                                              orientation_rpy[2])
        pose_target.position.x = position[0]
        pose_target.position.y = position[1]
        pose_target.position.z = position[2]
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]

        if arm_group == "right_arm":
            self.right_arm_group.set_planning_time(planning_time)
            self.right_arm_group.clear_pose_targets()
            self.right_arm_group.set_goal_position_tolerance(tolerance[0])
            self.right_arm_group.set_goal_orientation_tolerance(tolerance[1])
            self.right_arm_group.set_pose_reference_frame(ref_frame)
            self.right_arm_group.set_pose_target(pose_target)
            # DEBUG
            # plan = self.right_arm_group.plan()
            # rospy.loginfo(str(plan))
            self.right_arm_group.go(False)  # async_move

        elif arm_group == "left_arm":
            self.left_arm_group.set_planning_time(planning_time)
            self.left_arm_group.clear_pose_targets()
            self.left_arm_group.set_goal_position_tolerance(tolerance[0])
            self.left_arm_group.set_goal_orientation_tolerance(tolerance[1])
            self.left_arm_group.set_pose_reference_frame(ref_frame)
            self.left_arm_group.set_pose_target(pose_target)
            self.left_arm_group.go(False)  # async_movel
        else:
            rospy.logwarn("No specified arm_group")

    def get_joint_status(self, arm_group):
        joint_state = {}
        group_joint_names = None
        group_current_joint_values = None

        if arm_group == "right_arm":
            group_joint_names = self.right_arm_group.get_joints()
            group_current_joint_values = self.right_arm_group.get_current_joint_values()
        elif arm_group == "left_arm":
            group_joint_names = self.left_arm_group.get_joints()
            group_current_joint_values = self.left_arm_group.get_current_joint_values()
        elif arm_group == "right_gripper":
            group_joint_names = self.right_gripper_group.get_joints()
            group_current_joint_values = self.right_gripper_group.get_current_joint_values()
        elif arm_group == "left_gripper":
            group_joint_names = self.left_gripper_group.get_joints()
            group_current_joint_values = self.left_gripper_group.get_current_joint_values()
        else:
            rospy.logwarn("No specified arm_group")

        for i in range(0, len(group_joint_names)):
            joint_state[group_joint_names[i]] = group_current_joint_values[i]

        return joint_state

    def move_relative(self, arm_group, rel, relative_goal_translation, relative_goal_rotation):
        # respect to efflink
        if arm_group == "right_arm":
            last_pose = self.right_arm_group.get_current_pose()
            rospy.loginfo(str(type(last_pose)) + '\n' + str(last_pose))
            rpy = tf.transformations.euler_from_quaternion([last_pose.pose.orientation.x,
                                                            last_pose.pose.orientation.y,
                                                            last_pose.pose.orientation.z,
                                                            last_pose.pose.orientation.w])
            new_pose_translation = [last_pose.pose.position.x + relative_goal_translation[0],
                                    last_pose.pose.position.y + relative_goal_translation[1],
                                    last_pose.pose.position.z + relative_goal_translation[2]]
            new_pose_rotation = [rpy[0] + relative_goal_rotation[0], rpy[1] + relative_goal_rotation[1],
                                 rpy[2] + relative_goal_rotation[2]]
            self.manipulate(arm_group, new_pose_translation, new_pose_rotation)

    def set_joint(self, joint_name, joint_value):
        if (type(joint_name) == str) and (type(joint_value) == float):
            if "right" in joint_name:
                if "gripper" in joint_name:
                    self.right_gripper_group.set_joint_value_target(joint_name, joint_value)
                else:
                    self.right_arm_group.set_joint_value_target(joint_name, joint_value)
            elif "left" in joint_name:
                if "gripper" in joint_name:
                    self.left_gripper_group.set_joint_value_target(joint_name, joint_value)
                else:
                    self.left_arm_group.set_joint_value_target(joint_name, joint_value)
            else:
                rospy.logwarn("Controller : No specified Joint is Found")
                return False
            return True
        elif (type(joint_name) == list) and (type(joint_value) == list) and (len(joint_value) == len(joint_name)):
            for i in range(0, len(joint_value)):
                success = self.set_joint(joint_name[i], joint_value[i])
                if success:
                    return False
        else:
            rospy.logwarn("Invalid Argument")

    def move_joint(self, joint_name, joint_value):
        if "right" in joint_name:
            if "gripper" in joint_name:
                self.right_gripper_group.clear_pose_targets()
                self.set_joint(joint_name, joint_value)
                self.right_gripper_group.go(False)
            else:
                print self.right_arm_group
                if self.right_arm_group.clear_pose_targets() is not None:
                    self.right_arm_group.clear_pose_targets()
                self.set_joint(joint_name, joint_value)
                self.right_arm_group.go(False)

        elif "left" in joint_name:
            if "gripper" in joint_name:
                self.left_gripper_group.clear_pose_targets()
                self.set_joint(joint_name, joint_value)
                self.left_gripper_group.go(False)
            else:
                self.left_arm_group.clear_pose_targets()
                self.set_joint(joint_name, joint_value)
                self.left_arm_group.go(False)
        else:
            rospy.logwarn("Controller : No specified Joint is Found")
            return False
        return True

    # PICKING PROCEDURE
    # pregrasp -> open_gripper -> reach -> grasp
    def pickobject_init(self, arm_group, object_name, ref_frame="base_link"):
        self.pick_state["arm_group"] = arm_group
        self.pick_state["object_name"] = object_name
        # self.pick_state["laststate"] = "pregrasp"
        self.pick_state["ref_frame"] = ref_frame
        self.static_pose(self.pick_state["arm_group"], 'right_init_picking_normal')
        # rospy.loginfo('---------------------------pick object_init')

    def pickobject_prepare(self):
        # rospy.loginfo('prepare pregrasp')
        # self.pick_state["laststate"] = "prepare"
        self.static_pose(self.pick_state["arm_group"], 'right_picking_prepare')
        # rospy.loginfo('---------------------------pick object_prepare')

    def pickobject_pregrasp(self, object_position):
        # rospy.loginfo('pregrasp')
        # self.pick_state["laststate"] = "pregrasp"
        self.pick_state["object_position"] = object_position

        if object_position[0] >= 0.6:
            self.pregrasp_distance_x = 0.2
        else:
            self.pregrasp_distance_x = 0.1

        if object_position[1] >= 0.2 or object_position[1] <= -0.2:
            self.pregrasp_distance_y = 0.1
        else:
            self.pregrasp_distance_y = 0

        self.object_position.x = object_position[0]
        self.object_position.y = object_position[1]
        self.object_position.z = object_position[2]
        self.static_pose(self.pick_state["arm_group"], 'right_picking_pregrasp')
        rospy.loginfo('---pick_object_pregrasp---')

    def pickobject_movetoobjectfront_1(self, tolerance=[0.05, 0.1], pregrasp_direction=[1.0, 0, 0]):
        # TODO -- pregrasp in any direction, current x only
        pregraspposition = []
        self.pregrasp_value_x = self.pregrasp_distance_x
        pregraspposition.append(self.pregrasp_value_x)
        pregraspposition.append(self.pick_state["objectposition"][1])
        pregraspposition.append(self.pick_state["objectposition"][2])
        # self.pick_state["laststate"] = "pregrasp"
        # print pregraspposition
        if self.pick_state["arm_group"] is not None:
            self.manipulate(self.pick_state["arm_group"], pregraspposition)
        else:
            rospy.logwarn('manipulator_controller.pick_state arm_group is None')

        rospy.loginfo('--------------------------------------move to object front1')

    def pickobject_movetoobjectfront_2(self, tolerance=[0.05, 0.1], pregrasp_direction=[1.0, 0, 0]):
        # TODO -- pregrasp in any direction, current x only
        pregraspposition = []
        self.pregrasp_value_x = self.pregrasp_distance_x + self.pregrasp_value_x
        pregraspposition.append(self.pregrasp_value_x)
        pregraspposition.append(self.pick_state["objectposition"][1])
        pregraspposition.append(self.pick_state["objectposition"][2])
        # self.pick_state["laststate"] = "pregrasp"
        # print pregraspposition
        self.manipulate(self.pick_state["arm_group"], pregraspposition)
        rospy.loginfo('--------------------------------------move to object front2')

    def pickobject_movetoobjectfront_3(self, tolerance=[0.05, 0.1], pregrasp_direction=[1.0, 0, 0]):
        # TODO -- pregrasp in any direction, current x only
        pregraspposition = []
        pregraspposition.append(self.pick_state["objectposition"][0])
        pregraspposition.append(self.pick_state["objectposition"][1])
        pregraspposition.append(self.pick_state["objectposition"][2])
        # self.pick_state["laststate"] = "pregrasp"
        # print pregraspposition
        self.manipulate(self.pick_state["arm_group"], pregraspposition)
        rospy.loginfo('--------------------------------------move to object front3')

    def pickobject_opengripper(self):
        # open gripper
        if self.pick_state["arm_group"] == 'right_arm':
            self.move_joint("right_gripper_joint", GRIPPER_OPENED)
            # self.delay.wait(5000) # TODO: delay should not be here
            # self.static_pose(self.pick_state["right_gripper"], 'right_gripper_open')
            # print '>>loop<<'

            # elif self.pick_state["arm_group"] == 'left_arm':
            #     pass
            # self.move_joint("left_gripper_joint", GRIPPER_OPENED)
        rospy.loginfo('------------------------------open gripper')
        pass

    def pickobject_reach(self, tolerance=[0.05, 0.1], step=0.05):
        self.pick_state["laststate"] = "reach"
        waypoint = []
        target_pose = Pose()
        target_pose.position.x = self.pick_state["objectposition"][0] + 0.3
        target_pose.position.y = self.pick_state["objectposition"][1]
        target_pose.position.z = self.pick_state["objectposition"][2]
        start_pose = self.right_arm_group.get_current_pose().pose
        waypoint.append(start_pose)
        waypoint.append(target_pose)
        if self.pick_state["arm_group"] == "right_arm":
            # self.right_arm_group.clear_pose_targets()
            # self.right_arm_group.set_goal_position_tolerance(0.05)
            # self.right_arm_group.set_goal_orientation_tolerance(0.1)
            rospy.loginfo('point : ' + str(self.pick_state["objectposition"][0]) + ' ' + str(
                self.pick_state["objectposition"][1]) + ' ' + str(self.pick_state["objectposition"][2]))
            self.manipulate(self.pick_state["arm_group"], self.pick_state["objectposition"], [0, 0, 0], tolerance)
            # self.right_arm_group.go(False)
            # (path, fraction) = self.right_arm_group.compute_cartesian_path(waypoint, step, 0.00, True)
            # self.right_arm_group.execute(path)
        elif self.pick_state["arm_group"] == "left_arm":
            self.left_arm_group.clear_pose_targets()
            self.left_arm_group.set_goal_position_tolerance(0.01)
            self.left_arm_group.set_goal_orientation_tolerance(0.05)
            (path, fraction) = self.left_arm_group.compute_cartesian_path(waypoint, step, 0.00, True)
            self.left_arm_group.execute(path)

    def pickobject_grasp(self):
        # close gripper
        # self.pick_state["laststate"] = "closegripper"
        if self.pick_state["arm_group"] == "right_gripper":
            # if self.pick_state["demo"] == False:
            # self.set_torque_limit["right_gripper"](GRIPPER_EFFORT)
            self.static_pose(self.pick_state["arm_group"], 'right_gripper_close')
        elif self.pick_state["arm_group"] == "left_arm":
            # if self.pick_state["demo"] == False:
            # self.set_torque_limit["left_gripper"](GRIPPER_EFFORT)
            self.move_joint("left_gripper_joint", GRIPPER_CLOSED)

    def pickobject_after_grasp(self, shoulder_offset=0.2, elbow_offset=0.1, tolerance=[0.05, 0.1]):
        ## + shoulderoffset && fix wrist tobe zero
        self.pick_state["laststate"] = "aftergrasp"

        if self.pick_state["arm_group"] == "right_arm":
            self.right_arm_group.clear_pose_targets()
            # group_joint_names = self.right_arm_group.get_joints()
            # group_current_joint_values = self.right_arm_group.get_current_joint_values()
            joint_status = self.get_joint_status(self.pick_state["arm_group"])
            rospy.loginfo(str(joint_status))

            # for i in range(0,len(group_joint_names)):
            #     if group_joint_names[i] == 'right_shoulder_1_joint':
            #         self.setjoint(group_joint_names[i],group_current_joint_values[i] - shoulder_offset)
            #     elif group_joint_names[i] == 'right_shoulder_2_joint':
            #         self.setjoint(group_joint_names[i],group_current_joint_values[i])
            #     elif group_joint_names[i] == 'right_elbow_joint':
            #         if group_current_joint_values[i] >= 0.00:
            #             self.setjoint('right_elbow_joint',URDF_ELBOW_LIMIT)
            #         else:
            #             self.setjoint(group_joint_names[i],group_current_joint_values[i] + elbow_offset)
            #     else :
            #         self.setjoint(group_joint_names[i],group_current_joint_values[i])

            self.set_joint("right_shoulder_1_joint", joint_status["right_shoulder_1_joint"] - shoulder_offset)
            self.set_joint("right_shoulder_2_joint", joint_status["right_shoulder_2_joint"])
            if joint_status["right_elbow_joint"] >= 0.00:
                self.set_joint('right_elbow_joint', URDF_ELBOW_LIMIT)
            else:
                self.set_joint("right_elbow_joint", joint_status["right_elbow_joint"] + elbow_offset)
            self.set_joint('right_wrist_1_joint', 0.00)
            self.set_joint('right_wrist_2_joint', URDF_WRIST2_LIMIT)
            self.set_joint('right_wrist_3_joint', 0.00)
            self.right_arm_group.go(False)

        elif self.pick_state["arm_group"] == "left_arm":
            self.left_arm_group.clear_pose_targets()

    def pick_object_finish(self, tolerance=[0.05, 0.1]):
        # To its normal position
        self.pick_state["laststate"] = "finish"

        self.pick_state["object_name"] = None
        self.pick_state["arm_group"] = None
        self.pick_state["objectposition"] = None
        self.pick_state["ref_frame"] = None
        if self.pick_state["arm_group"] == "right_arm":
            self.static_pose("right_arm", "right_normal")
        elif self.pick_state["arm_group"] == "left_arm":
            self.static_pose("left_arm", "left_normal")

    def pick(self, arm_group, position, orientation_rpy=[0, 0, 0], desired_object="part", support_surface_name="table",
             ref_frame="base_link", planning_time=300.00, grasp_constraint=None):

        pose_target = geometry_msgs.msg.PoseStamped()

        pose_target.header.frame_id = ref_frame
        quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0],
                                                              orientation_rpy[1],
                                                              orientation_rpy[2])
        pose_target.pose.orientation.x = quaternion[0]
        pose_target.pose.orientation.y = quaternion[1]
        pose_target.pose.orientation.z = quaternion[2]
        pose_target.pose.orientation.w = quaternion[3]
        pose_target.pose.position.x = position[0]
        pose_target.pose.position.y = position[1]
        pose_target.pose.position.z = position[2]
        # Generate a list of grasps
        grasp = self.make_grasps(pose_target, desired_object, [-0.2])

        if arm_group == "right_arm":
            self.right_arm_group.set_support_surface_name(support_surface_name)
            self.right_arm_group.set_goal_position_tolerance(0.01)
            self.right_gripper_group.set_goal_position_tolerance(0.01)
            self.right_arm_group.set_goal_orientation_tolerance(0.05)
            self.right_gripper_group.set_goal_orientation_tolerance(0.05)
            self.right_arm_group.set_planning_time(planning_time)
            self.right_arm_group.pick(desired_object, grasp)
        elif arm_group == "left_arm":
            self.left_arm_group.set_support_surface_name(support_surface_name)
            self.left_arm_group.set_goal_position_tolerance(0.01)
            self.left_arm_group.set_goal_orientation_tolerance(0.05)
            self.left_arm_group.set_planning_time(planning_time)
            self.left_arm_group.pick(desired_object, grasp)
        else:
            rospy.logwarn("No specified arm_group")

    def make_gripper_posture(self, joint_positions):
        # Initialize the joint trajectory for the gripper joints
        t = trajectory_msgs.msg.JointTrajectory()

        # Set the joint names to the gripper joint names
        t.joint_names = GRIPPER_JOINT_NAMES

        # Initialize a joint trajectory point to represent the goal
        tp = trajectory_msgs.msg.JointTrajectoryPoint()

        # Assign the trajectory joint positions to the input positions
        tp.positions = joint_positions

        # Set the gripper effort
        tp.effort = GRIPPER_EFFORT

        tp.time_from_start = rospy.Duration(1.0)

        # Append the goal point to the trajectory points
        t.points.append(tp)

        # Return the joint trajectory
        return t

    # Generate a gripper translation in the direction given by vector
    def make_gripper_translation(self, min_dist, desired, vector, frame):
        # Initialize the gripper translation object
        g = moveit_msgs.msg.GripperTranslation()

        # Set the direction vector components to the input
        g.direction.vector.x = vector[0]
        g.direction.vector.y = vector[1]
        g.direction.vector.z = vector[2]

        # The vector == relative to the gripper frame
        # g.direction.header.frame_id = GRIPPER_FRAME
        g.direction.header.frame_id = frame

        # Assign the min and desired distances from the input
        g.min_distance = min_dist
        g.desired_distance = desired

        return g

    # Generate a list of possible grasps
    def make_grasps(self, initial_pose_stamped, allowed_touch_objects, grasp_opening=[0]):
        # Initialize the grasp object
        g = moveit_msgs.msg.Grasp()

        # Set the pre-grasp and grasp postures appropriately;
        # grasp_opening should be a bit smaller than target width
        g.pre_grasp_posture = self.make_gripper_posture(GRIPPER_OPENED)
        g.grasp_posture = self.make_gripper_posture(grasp_opening)

        # Set the approach and retreat parameters as desired
        # g.pre_grasp_approach = self.make_gripper_translation(0.01, 0.1, [1.0, 0.0, 0.0])
        # g.post_grasp_retreat = self.make_gripper_translation(0.1, 0.15, [-1.0, 0.0, 0.0])

        g.pre_grasp_approach = self.make_gripper_translation(0.1, 0.25, [1.0, 0.0, 0.0], GRIPPER_FRAME)
        g.post_grasp_retreat = self.make_gripper_translation(0.0, 0.0, [0.0, 0.0, 1.0], "right_wrist_3_Link")
        # Set the first grasp pose to the input pose
        g.grasp_pose = initial_pose_stamped

        # Pitch angles to try
        pitch_vals = [0, 0.1, -0.1, 0.2, -0.2, 0.4, -0.4]

        # Yaw angles to try
        yaw_vals = [0]

        # A list to hold the grasps
        grasps = []

        # Generate a grasp for each pitch and yaw angle
        for y in yaw_vals:
            for p in pitch_vals:
                # Create a quaternion from the Euler angles
                q = tf.transformations.quaternion_from_euler(0, p, y)

                # Set the grasp pose orientation accordingly
                g.grasp_pose.pose.orientation.x = q[0]
                g.grasp_pose.pose.orientation.y = q[1]
                g.grasp_pose.pose.orientation.z = q[2]
                g.grasp_pose.pose.orientation.w = q[3]

                # Set and id for this grasp (simply needs to be unique)
                g.id = str(len(grasps))

                # Set the allowed touch objects to the input list
                g.allowed_touch_objects = allowed_touch_objects

                # Don't restrict contact force
                g.max_contact_force = 0

                # Degrade grasp quality for increasing pitch angles
                g.grasp_quality = 1.0 - abs(p)

                # Append the grasp to the list
                grasps.append(deepcopy(g))

        # Return the list
        return grasps

    # Generate a list of possible place poses
    def make_places(self, init_pose):
        # Initialize the place location as a PoseStamped message
        place = geometry_msgs.msg.PoseStamped()

        # Start with the input place pose
        place = init_pose

        # A list of x shifts (meters) to try
        x_vals = [0, 0.005, 0.01, 0.015, -0.005, -0.01, -0.015]

        # A list of y shifts (meters) to try
        y_vals = [0, 0.005, 0.01, 0.015, -0.005, -0.01, -0.015]

        # A list of pitch angles to try
        # pitch_vals = [0, 0.005, -0.005, 0.01, -0.01, 0.02, -0.02]

        pitch_vals = [0]

        # A list of yaw angles to try
        yaw_vals = [0]

        # A list to hold the places
        places = []

        # Generate a place pose for each angle and translation
        for y in yaw_vals:
            for p in pitch_vals:
                for y in y_vals:
                    for x in x_vals:
                        place.pose.position.x = init_pose.pose.position.x + x
                        place.pose.position.y = init_pose.pose.position.y + y

                        # Create a quaternion from the Euler angles
                        q = tf.transformations.quaternion_from_euler(0, p, y)

                        # Set the place pose orientation accordingly
                        place.pose.orientation.x = q[0]
                        place.pose.orientation.y = q[1]
                        place.pose.orientation.z = q[2]
                        place.pose.orientation.w = q[3]

                        # Append this place pose to the list
                        places.append(deepcopy(place))

        # Return the list
        return places

    def static_pose(self, arm_group, posture, tolerance=[0.05, 0.1]):
        if arm_group == "right_arm":
            self.right_arm_group.clear_pose_targets()
            self.right_arm_group.set_goal_position_tolerance(tolerance[0])
            self.right_arm_group.set_goal_orientation_tolerance(tolerance[1])
            self.right_arm_group.set_named_target(posture)
            self.right_arm_group.go(False)  # async_move
        elif arm_group == "left_arm":
            self.left_arm_group.clear_pose_targets()
            self.left_arm_group.set_goal_position_tolerance(tolerance[0])
            self.left_arm_group.set_goal_orientation_tolerance(tolerance[1])
            self.left_arm_group.set_named_target(posture)
            self.left_arm_group.go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group1")

    def __del__(self):
        # Deconstructor should be call before shutdown nodes
        moveit_commander.roscpp_shutdown()
