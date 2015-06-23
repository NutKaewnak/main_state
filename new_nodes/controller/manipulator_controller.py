__author__ = "kandithws"

import rospy
import moveit_commander
import moveit_msgs.msg
import std_msgs.msg
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import tf
import sys
from copy import deepcopy
from dynamixel_controllers.srv import SetTorqueLimit

GRIPPER_FRAME = 'right_wrist_3_Link'
GRIPPER_JOINT_NAMES = ['right_gripper_joint']
 
GRIPPER_OPENED = 0.0
GRIPPER_CLOSED = -0.6
GRIPPER_NEUTRAL = 0.0
GRASP_OVERTIGHTEN = -0.01
GRIPPER_EFFORT = 0.4
 
REFERENCE_FRAME = 'base_link'


class ManipulateController:
    def __init__(self):
        # group should be "left_arm" or "right_arm"
        # self.moveit_commander.roscpp_initialize(" ")
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.pickstate = {}
        self.pickstate["objectname"] = None
        self.pickstate["arm_group"] = None
        self.pickstate["objectposition"] = None
        self.pickstate["laststate"] = None
        self.pickstate["demo"] = False
        self.settorquelimit = {}
        try:
            self.settorquelimit["right_gripper"] = rospy.ServiceProxy('/dynamixel/right_gripper/set_torque_limit', SetTorqueLimit)
            self.settorquelimit["left_gripper"] = rospy.ServiceProxy('/dynamixel/left_gripper/set_torque_limit', SetTorqueLimit)
            #Test if there is service avaliable
            self.settorquelimit["right_gripper"](GRIPPER_EFFORT)
        except rospy.ServiceException, e:
            rospy.loginfo("Service call failed: Running DEMO MODE")
            self.pickstate["demo"] = True


        # self.group = self.moveit_commander.MoveGroupCommander(arm_group)
        # self.group.set_planning_time(planning_time)
        self.grasp_plan = None

    def __del__(self):
        # Deconstructor should be call before shutdown nodes
        moveit_commander.roscpp_shutdown()

    def manipulate(self, arm_group, position, orientation_rpy=[0, 0, 0], ref_frame="base_link", planning_time=100.00):
        pose_target = geometry_msgs.msg.Pose()
        quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0],
                                                              orientation_rpy[1],
                                                              orientation_rpy[2])
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]
        pose_target.position.x = position[0]
        pose_target.position.y = position[1]
        pose_target.position.z = position[2]

        if arm_group is "right_arm":
            self.robot.right_arm.set_planning_time(planning_time)
            self.robot.right_arm.clear_pose_targets()
            self.robot.right_arm.set_pose_reference_frame(ref_frame)
            self.robot.right_arm.set_pose_target(pose_target)
            self.robot.right_arm.go(False)  # async_move

        elif arm_group is "left_arm":
            self.robot.left_arm.set_planning_time(planning_time)
            self.robot.left_arm.clear_pose_targets()
            self.robot.left_arm.set_pose_reference_frame(ref_frame)
            self.robot.left_arm.set_pose_target(pose_target)
            self.robot.left_arm.go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group")

    def setjoint(self,jointname,jointvalue):
        if (type(jointname) is str) and (type(jointvalue) is float):
            if jointname.find("right") is not -1:
                if jointname.find("gripper") is not -1:
                    self.robot.right_gripper.set_joint_value_target(jointname,jointvalue)
                else:
                    self.robot.right_arm.set_joint_value_target(jointname,jointvalue)
            elif jointname.find("left") is not -1: 
                if jointname.find("gripper") is not -1:
                    self.robot.left_gripper.set_joint_value_target(jointname,jointvalue)
                else:
                    self.robot.left_arm.set_joint_value_target(jointname,jointvalue)
            else:
                rospy.logwarn("Controller : No specified Joint is Found")
                return False
            return True
        elif (type(jointname) is list) and (type(jointvalue) is list) and (len(jointvalue) == len(jointname)):
            for i in range(0,len(jointvalue)):
                success = self.setjoint(jointname[i],jointvalue[i])
                if success is False:
                    return False
        else:
            rospy.logwarn("Invalid Argument")

    def movejoint(self,jointname,jointvalue):
        if jointname.find("right") is not -1:
            if jointname.find("gripper") is not -1:
                self.robot.right_gripper.clear_pose_targets()
                self.setjoint(jointname,jointvalue)
                self.robot.right_gripper.go(False)
            else:
                self.robot.right_arm.clear_pose_targets(False)
                self.setjoint(jointname,jointvalue)
                self.robot.right_arm.go(False)

        elif jointname.find("left") is not -1: 
            if jointname.find("gripper") is not -1:
                self.robot.left_gripper.clear_pose_targets()
                self.setjoint(jointname,jointvalue)
                self.robot.left_gripper.go(False)
            else:
                self.robot.left_arm.clear_pose_targets(False)
                self.setjoint(jointname,jointvalue)
                self.robot.left_arm.go(False)
        else:
            rospy.logwarn("Controller : No specified Joint is Found")
            return False
        return True
        
    ### PICKING PROCEDURE
    ### pregrasp -> opengripper -> reach -> grasp
   
    def pickobject_pregrasp(self,arm_group,objectname,objectposition,pregrasp_distance = 0.3,pregrasp_direction = [1.0,0,0],ref_frame = "base_link"):
        ##TODO -- pregrasp in any direction, current x only
        pregraspposition = []
        pregraspposition.append(objectposition[0] - pregrasp_distance)
        pregraspposition.append(objectposition[1])
        pregraspposition.append(objectposition[2])
        self.pickstate["objectname"] = objectname
        self.pickstate["arm_group"] = arm_group
        self.pickstate["objectposition"] = objectposition
        self.pickstate["laststate"] = "pregrasp"
        self.manipulate(arm_group,pregraspposition)
        rospy.loginfo("Moving"+ arm_group + "to x = " + str(pregraspposition[0]) + " ,y = " + str(pregraspposition[1]) + " ,z= " + str(pregraspposition[2]) + "\n respect to " + ref_frame  )


    def pickobject_opengripper(self):
        ##opengripper
        self.pickstate["laststate"] = "opengripper"
        if self.pickstate["arm_group"] is "right_arm":
            self.movejoint("right_gripper_joint",GRIPPER_OPENED)
        elif self.pickstate["arm_group"] is "left_arm":
            self.movejoint("left_gripper_joint",GRIPPER_OPENED)


    def pickobject_reach(self,step=0.05):
        self.pickstate["laststate"] = "reach"
        waypoint = []
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = self.pickstate["objectposition"][0]
        target_pose.position.y = self.pickstate["objectposition"][1]
        target_pose.position.z = self.pickstate["objectposition"][2]
        start_pose = self.robot.right_arm.get_current_pose().pose
        waypoint.append(start_pose)
        waypoint.append(target_pose)
        if self.pickstate["arm_group"] is "right_arm":
            self.robot.right_arm.clear_pose_targets()
            self.robot.right_arm.set_goal_position_tolerance(0.01)
            self.robot.right_arm.set_goal_orientation_tolerance(0.1)
            (path,fraction) = self.robot.right_arm.compute_cartesian_path(waypoint,step,0.00,True)
            self.robot.right_arm.execute(path)
        elif self.pickstate["arm_group"] is "left_arm":
            self.robot.left_arm.clear_pose_targets()
            self.robot.left_arm.set_goal_position_tolerance(0.01)
            self.robot.left_arm.set_goal_orientation_tolerance(0.1)
            (path,fraction) = self.robot.left_arm.compute_cartesian_path(waypoint,step,0.00,True)
            self.robot.left_arm.execute(path)
            
    


    def pickobject_grasp(self):
        ##closegripper
        self.pickstate["laststate"] = "closegripper"
        if self.pickstate["arm_group"] is "right_arm":
            if self.pickstate["demo"] is False:
                self.settorquelimit["right_gripper"](GRIPPER_EFFORT)
            self.movejoint("right_gripper_joint",GRIPPER_CLOSED)
        elif self.pickstate["arm_group"] is "left_arm":
            if self.pickstate["demo"] is False:
                self.settorquelimit["left_gripper"](GRIPPER_EFFORT)
            self.movejoint("left_gripper_joint",GRIPPER_CLOSED)
    
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
        
        # if grasp_constraint is None:
        #     grasp_constraint = moveit_msgs.msg.Grasp()
        #     grasp_constraint.grasp_pose = pose_target

        #     grasp_constraint.pre_grasp_approach.direction.vector.x = 1.0
        #     grasp_constraint.pre_grasp_approach.direction.header.frame_id = "right_wrist_3_Link"
        #     #grasp_constraint.pre_grasp_approach.direction.header.frame_id = "left_wrist_3_Link"
        #     grasp_constraint.pre_grasp_approach.min_distance = 0.1
        #     grasp_constraint.pre_grasp_approach.desired_distance = 0.25

        #     # Retreat directly move_back
        #     grasp_constraint.post_grasp_retreat.direction.header.frame_id = "right_wrist_3_Link"
        #     #grasp_constraint.post_grasp_retreat.direction.vector.x = -1.0
        #     grasp_constraint.post_grasp_retreat.direction.vector.z = 1.0
        #     grasp_constraint.post_grasp_retreat.min_distance = 0.00
        #     grasp_constraint.post_grasp_retreat.desired_distance = 0.00

        #     # open_gripper
        #     grasp_constraint.pre_grasp_posture.joint_names.append("right_gripper_joint")
        #     #grasp_constraint.pre_grasp_posture.joint_names.append("left_gripper_joint")
        #     grasp_constraint.pre_grasp_posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        #     grasp_constraint.pre_grasp_posture.points[0].positions.append(std_msgs.msg.Float64())
        #     grasp_constraint.pre_grasp_posture.points[0].positions[0] = 0

        #     # close_gripper
        #     grasp_constraint.grasp_posture.joint_names.append("right_gripper_joint")
        #     #grasp_constraint.grasp_posture.joint_names.append("left_gripper_joint")
        #     grasp_constraint.grasp_posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
        #     grasp_constraint.grasp_posture.points[0].positions.append(std_msgs.msg.Float64())
        #     grasp_constraint.grasp_posture.points[0].positions[0] = -0.2

        #     grasp = [grasp_constraint]

        if arm_group is "right_arm":
            self.robot.right_arm.set_support_surface_name(support_surface_name)
            self.robot.right_arm.set_goal_position_tolerance(0.1)
            self.robot.right_gripper.set_goal_position_tolerance(0.1)
            self.robot.right_arm.set_goal_orientation_tolerance(0.1)
            self.robot.right_gripper.set_goal_orientation_tolerance(0.1)
            self.robot.right_arm.set_planning_time(planning_time)
            self.robot.right_arm.pick(desired_object, grasp)
        elif arm_group is "left_arm":
            self.robot.left_arm.set_support_surface_name(support_surface_name)
            self.robot.left_arm.set_goal_position_tolerance(0.1) 
            self.robot.left_arm.set_goal_orientation_tolerance(0.1)
            self.robot.left_arm.set_planning_time(planning_time)
            self.robot.left_arm.pick(desired_object, grasp)
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
    def make_gripper_translation(self, min_dist, desired, vector,frame):
        # Initialize the gripper translation object
        g = moveit_msgs.msg.GripperTranslation()
 
         # Set the direction vector components to the input
        g.direction.vector.x = vector[0]
        g.direction.vector.y = vector[1]
        g.direction.vector.z = vector[2]
 
        # The vector is relative to the gripper frame
        #g.direction.header.frame_id = GRIPPER_FRAME
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
        #g.pre_grasp_approach = self.make_gripper_translation(0.01, 0.1, [1.0, 0.0, 0.0])
        #g.post_grasp_retreat = self.make_gripper_translation(0.1, 0.15, [-1.0, 0.0, 0.0])
        
        g.pre_grasp_approach = self.make_gripper_translation(0.1, 0.25, [1.0, 0.0, 0.0],GRIPPER_FRAME)
        g.post_grasp_retreat = self.make_gripper_translation(0.0, 0.0, [0.0, 0.0, 1.0],"right_wrist_3_Link") 
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

    def static_pose(self, arm_group, posture):
        if arm_group is "right_arm":
            self.robot.right_arm.clear_pose_targets()
            self.robot.right_arm.set_named_target(posture)
            self.robot.right_arm.go(False)  # async_move
        elif arm_group is "left_arm":
            self.robot.left_arm.clear_pose_targets()
            self.robot.left_arm.set_named_target(posture)
            self.robot.left_arm.go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group")