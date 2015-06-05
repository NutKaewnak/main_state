__author__ = "AThousandYears"

from joint import Joint


class NeckController:
    def __init__(self):
        self.neck_motor = Joint('neck', ['neck_controller', 'pan_controller', 'tilt_controller'])
        self.set_neck_angle(0, 0) # set neck at 0 0 at start.
        self.pitch = 0
        self.yaw = 0

    def set_neck_angle(self, pitch, yaw):
        self.pitch = pitch
        self.yaw = yaw
        self.neck_motor.move_joint([0, pitch, yaw])

    # This method have another better solution and it will be implement next version.
    def set_neck_angle_relative(self, pitch, yaw):
        self.pitch += pitch
        self.yaw += yaw
        self.neck_motor.move_joint([0, pitch, yaw])
