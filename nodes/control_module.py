from controller.speaker import Speaker
from controller.base_controller import BaseController
from controller.neck_controller import NeckController
from controller.torso_controller import TorsoController
from controller.arm_controller import ArmController
from controller.manipulator_controller import ManipulateController
from controller.gripper_controller import GripperController
# from controller.recognize_objects_contoller import RecognizeObjectsObController

__author__ = "AThousandYears"


class ControlModule:
    speaker = Speaker()
    base = BaseController()
    neck = NeckController()
    torso = TorsoController()
    left_arm = ArmController("left")
    right_arm = ArmController("right")
    # recognize_objects = RecognizeObjectsObController()
    manipulator = ManipulateController()
    gripper = GripperController()

    def __init__(self):
        pass
