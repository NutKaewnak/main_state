__author__ = "AThousandYears"

from controller.speaker import Speaker
from controller.base_controller import BaseController
from controller.neck_controller import NeckController
from controller.torso_controller import TorsoController
from controller.arm_controller import ArmController
# from controller.manipulator_controller import ManipulateController


class ControlModule:
    speaker = Speaker()
    base = BaseController()
    neck = NeckController()
    torso = TorsoController()
    left_arm = ArmController("left")
    right_arm = ArmController("right")
    # manipulator = ManipulateController()

    def __init__(self):
        pass
