from controller.speaker import Speaker
from controller.base_controller import BaseController
from controller.neck_controller import NeckController
from controller.torso_controller import TorsoController
from controller.manipulator_controller import ManipulateController
from controller.recognize_objects_controller import RecognizeObjectsObController
from controller.object_3d_detector_controller import Object3dsDetectorController
from controller.voice_recognition_mode_controller import VoiceRecognitionModeController

__author__ = "AThousandYears"


class ControlModule:
    speaker = Speaker()
    base = BaseController()
    neck = NeckController()
    torso = TorsoController()
    left_arm = ManipulateController("left_arm")
    left_gripper = ManipulateController('right_left')
    right_arm = ManipulateController("right_arm")
    right_gripper = ManipulateController('right_gripper')
    recognize_objects = RecognizeObjectsObController()
    object_3d_detector = Object3dsDetectorController()
    voice_recognition_mode = VoiceRecognitionModeController()

    def __init__(self):
        pass
