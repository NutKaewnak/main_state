__author__ = "AThousandYears"

from joint_trajectory_follow import JointTrajectoryFollow


class NeckController:
    def __init__(self):
        self.neck_motor = JointTrajectoryFollow('neck_controller', ['tilt_joint', 'pan_joint'])
        self.set_neck_angle(0, 0)  # set neck at 0 0 at start.
        self.pitch = 0
        self.yaw = 0

    def set_neck_angle(self, pitch, yaw):
        self.pitch = pitch
        self.yaw = yaw
        self.neck_motor.move_joint([pitch, yaw])

    # This method have another better solution and it will be implement next version.
    def set_neck_angle_relative(self, pitch, yaw):
        self.pitch += pitch
        self.yaw += yaw
        self.neck_motor.move_joint([pitch, yaw])
