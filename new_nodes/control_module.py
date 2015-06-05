__author__ = "AThousandYears"

from controller.speaker import Speaker
from controller.base_controller import BaseController
from controller.neck_controller import NeckController
from controller.torso_controller import TorsoController
from controller.arm_controller import ArmController


class ControlModule:
    speaker = Speaker()
    base = BaseController()
    neck = NeckController()
    torso = TorsoController()
    left_arm = ArmController("left")
    right_arm = ArmController("right")

    def __init__(self):
        pass
