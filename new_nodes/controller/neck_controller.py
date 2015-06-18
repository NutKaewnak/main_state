__author__ = "AThousandYears"

from joint_trajectory_follow import JointTrajectoryFollow


class NeckController:
    def __init__(self):
        self.neck_motor = JointTrajectoryFollow('neck_controller', ['tilt_joint', 'pan_joint'])

    def set_neck_angle(self, pitch, yaw):
        self.neck_motor.move_joint([pitch, yaw])