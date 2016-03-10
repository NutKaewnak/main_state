import rospy
from dynamixel_controllers.srv import SetTorqueLimit


def set_torque_limit(limit=0.5):
    rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
    try:
        rospy.loginfo('settorque')
        setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
        respTorque = setTorque(limit)
    except rospy.ServiceException, e:
        rospy.logwarn("Service Torque call failed " + str(e))
