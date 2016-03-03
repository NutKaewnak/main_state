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

GRIPPER_OPENED = 0.8
GRIPPER_CLOSED = 0.0
GRIPPER_NEUTRAL = 0.0
GRASP_OVERTIGHTEN = -0.01
GRIPPER_EFFORT = 0.2
URDF_ELBOW_LIMIT = 0.2
URDF_WRIST2_LIMIT = -0.40

GRIPPER_PITCH_OFFSET = 0.2
EEF_OFFSET = []

REFERENCE_FRAME = 'base_link'

RIGHT_ARM = 'right_arm'
RIGHT_GRIPPER = 'right_gripper'
LEFT_ARM = 'left_arm'
LEFT_GRIPPER = 'left_gripper'


def get_joint_group(joint_name):
    """
    This function classified arm_group by joint_name
    :param joint_name: (string)
    :return arm_group: (string)
    """
    if "gripper" in joint_name:
        if "right" in joint_name:
            return RIGHT_GRIPPER
        elif "left" in joint_name:
            return LEFT_GRIPPER
    elif 'shoulder' in joint_name or 'elbow' in joint_name or 'wrist' in joint_name:
        if "right" in joint_name:
            return RIGHT_ARM
        elif "left" in joint_name:
            return LEFT_ARM
    else:
        rospy.logwarn("Controller : No specified Joint is Found")
        return False


class ManipulateController:
    def __init__(self):
        # group should be "left_arm" or "right_arm
        self.pick_state = {"arm_group": None,
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
        self.arm_groups = dict()
        self.tf_listener = None

    def init_controller(self):
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.tf_listener = tf.TransformListener()
        self.arm_groups[RIGHT_ARM] = moveit_commander.MoveGroupCommander(RIGHT_ARM)
        self.arm_groups[RIGHT_GRIPPER] = moveit_commander.MoveGroupCommander(RIGHT_GRIPPER)
        self.arm_groups[LEFT_ARM] = moveit_commander.MoveGroupCommander(LEFT_ARM)
        self.arm_groups[LEFT_GRIPPER] = moveit_commander.MoveGroupCommander(LEFT_GRIPPER)

    def transform_point(self, point_stamped, arm_group):
        """
        Transform point from origin frame (Default: 'base_link') to 'mani_link'
        :param point_stamped: (PointStamped)
        :param arm_group: (string)
        :return: (PointStamped), False if input arm_group is incorrect
        """
        destination_frame = None
        if arm_group == RIGHT_ARM:
            destination_frame = 'right_mani_link'
        elif arm_group == LEFT_ARM:
            destination_frame = 'left_mani_link'
        else:
            return False
        point_out = self.tf_listener.transform_point(destination_frame, point_stamped)
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

        if arm_group == RIGHT_ARM or arm_group == LEFT_ARM:
            self.arm_groups[arm_group].set_planning_time(planning_time)
            self.arm_groups[arm_group].clear_pose_targets()
            self.arm_groups[arm_group].set_goal_position_tolerance(tolerance[0])
            self.arm_groups[arm_group].set_goal_orientation_tolerance(tolerance[1])
            self.arm_groups[arm_group].set_pose_reference_frame(ref_frame)
            self.arm_groups[arm_group].set_pose_target(pose_target)
            self.arm_groups[arm_group].go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group")

    def get_joint_status(self, arm_group):
        joint_state = {}
        group_joint_names = None
        group_current_joint_values = None
        if arm_group == RIGHT_ARM or arm_group == LEFT_ARM:
            group_joint_names = self.arm_groups[arm_group].get_joints()
            group_current_joint_values = self.arm_groups[arm_group].get_current_joint_values()
        else:
            rospy.logwarn("No specified arm_group")
        for i in range(0, len(group_joint_names)):
            joint_state[group_joint_names[i]] = group_current_joint_values[i]
        return joint_state

    def move_relative(self, arm_group, relative_goal_translation, relative_goal_rotation):
        # respect to efflink
        if arm_group == RIGHT_ARM:
            last_pose = self.arm_groups[arm_group].get_current_pose()
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

    def move_joint(self, joint_name, joint_value):
        if (type(joint_name) == str) and (type(joint_value) == float):
            arm_group = get_joint_group(joint_name)
            if bool(arm_group):
                self.arm_groups[arm_group].clear_pose_targets()
                self.arm_groups[arm_group].set_joint_value_target(joint_name, joint_value)
                self.arm_groups[arm_group].go(False)
            else:
                return False
        else:
            rospy.logwarn("Invalid Argument")
            return False
        return True

    # PICKING PROCEDURE
    # pregrasp -> open_gripper -> reach -> grasp

    def pick_object_init(self, arm_group, ref_frame="base_link"):
        self.pick_state["arm_group"] = arm_group
        self.pick_state["ref_frame"] = ref_frame
        self.static_pose('right_init_picking_normal')
        rospy.loginfo('---------------------------pick object_init')

    def pickobject_pregrasp(self, object_position):
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
        self.static_pose('right_picking_pregrasp')
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

        rospy.loginfo('-------------------------------------move to object front1')

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
        rospy.loginfo('------------------move to object front2--------------------')

    def pickobject_movetoobjectfront_3(self, tolerance=[0.05, 0.1], pregrasp_direction=[1.0, 0, 0]):
        # TODO -- pregrasp in any direction, current x only
        pregraspposition = []
        pregraspposition.append(self.pick_state["objectposition"][0])
        pregraspposition.append(self.pick_state["objectposition"][1])
        pregraspposition.append(self.pick_state["objectposition"][2])
        # self.pick_state["laststate"] = "pregrasp"
        # print pregraspposition
        self.manipulate(self.pick_state["arm_group"], pregraspposition)
        rospy.loginfo('------------------move to object front3--------------------')

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

    def pick(self, arm_group, position, orientation_rpy=[0, 0, 0], desired_object="part", support_surface_name="table",
             ref_frame="base_link", planning_time=300.00, grasp_constraint=None):

        pose_target = PointStamped()

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
        place = PoseStamped()

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

    def move_arm_group(self, angles):
        """
        Move array of arm joints with specific angle.
        :param angles: (dict()) dict of angle and arm_joint
        :return: (None)
        """
        for x in angles:
            self.move_joint(x, angles[x])

    def static_pose(self, posture, tolerance=[0.05, 0.1]):
        if 'right' in posture:
            arm_group = RIGHT_ARM
        elif 'left' in posture:
            arm_group = LEFT_ARM

        if arm_group == RIGHT_ARM or arm_group == LEFT_ARM:
            self.arm_groups[arm_group].clear_pose_targets()
            self.arm_groups[arm_group].set_goal_position_tolerance(tolerance[0])
            self.arm_groups[arm_group].set_goal_orientation_tolerance(tolerance[1])
            self.arm_groups[arm_group].set_named_target(posture)
            self.arm_groups[arm_group].go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group")

    def __del__(self):
        # Deconstructor should be call before shutdown nodes
        moveit_commander.roscpp_shutdown()
