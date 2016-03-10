import tf
import sys
import rospy
import moveit_commander


class MoveItInitiator(object):
    class _MoveItInitiator:
        def __init__(self):
            moveit_commander.roscpp_initialize(sys.argv)
            self.robot = moveit_commander.RobotCommander()
            self.scene = moveit_commander.PlanningSceneInterface()
            self.tf_listener = tf.TransformListener()

        def init_controller(self, arm_group):
            print arm_group
            print arm_group in self.robot.get_group_names()
            return moveit_commander.MoveGroupCommander(arm_group)

        def __del__(self):
            moveit_commander.roscpp_shutdown()

    instance = None
    # def __init__(self):
    #     MoveItInitiator.instance = None

    def __new__(cls, *args, **kwargs):
        if not MoveItInitiator.instance:
            MoveItInitiator.instance = MoveItInitiator._MoveItInitiator()
        return MoveItInitiator.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

