from controller.speaker import Speaker
from controller.base_controller import BaseController
from controller.neck_controller import NeckController
from controller.torso_controller import TorsoController
from controller.gripper_action_controller import GripperActionController
from controller.manipulator_controller import ManipulateController
from controller.recognize_objects_controller import RecognizeObjectsObController
from controller.object_3d_detector_controller import Object3dsDetectorController
from controller.voice_recognition_mode_controller import VoiceRecognitionModeController
from controller.clothes_detector_controller import ClothesDetectorController
from controller.sound_player import SoundPlayer

__author__ = "AThousandYears"


class ControlModule:
    speaker = Speaker()
    base = BaseController()
    neck = NeckController()
    torso = TorsoController()
    left_gripper = GripperActionController("left_gripper")
    left_arm = ManipulateController("left_arm")
    right_gripper = GripperActionController("right_gripper")
    right_arm = ManipulateController("right_arm")
    recognize_objects = RecognizeObjectsObController()
    object_3d_detector = Object3dsDetectorController()
    voice_recognition_mode = VoiceRecognitionModeController()
    cloth_detector = ClothesDetectorController()
    sound_player = SoundPlayer()

    def __init__(self):
        pass
