from perception.delay import Delay
from perception.door_detect import DoorDetection
from perception.include.devices import Devices
from perception.base_status import BaseStatusPerception
from perception.voice import VoicePerception
from perception.gesture_detect import GestureDetection
from perception.neck import Neck
from perception.people_detect import PeopleDetection
from perception.object_3ds_detector_status import Object3DsDetectorPerception
from perception.right_arm import RightArm
from perception.right_gripper import RightGripper
from perception.left_arm import LeftArm
from perception.circle_detection import CircleDetection
from perception.height import Height
# from perception.joy import JoyInput
from perception.clothes_detector_status import ClothesDetectorPerception
from perception.recognize_objects_status import RecognizeObjectsPerception
from perception.voice_recognition_mode_status import VoiceRecognitionModePerception
from perception.people_leg_detect import PeopleLegDetection
__author__ = "AThousandYears"


class PerceptionModule:

    def __init__(self, main_state):
        self.delay = Delay()
        self.Devices = Devices
        self.base_status = BaseStatusPerception(main_state.planningModule)
        self.voice = VoicePerception(main_state.planningModule)
        self.gesture = GestureDetection(main_state.planningModule)
        self.neck = Neck(main_state.planningModule)
        self.door = DoorDetection(main_state.planningModule)
        self.people = PeopleDetection(main_state.planningModule)
        self.object_3ds_detector = Object3DsDetectorPerception(main_state.planningModule)
        self.right_arm = RightArm(main_state.planningModule)
        self.right_gripper = RightGripper(main_state.planningModule)
        self.left_arm = LeftArm(main_state.planningModule)
        self.circle_detection = CircleDetection(main_state.planningModule)
        self.height = Height(main_state.planningModule)
        # self.joy = JoyInput(main_state.planningModule)
        self.recosgnize_objects = RecognizeObjectsPerception(main_state.planningModule)
        self.voice_recognition_mode = VoiceRecognitionModePerception(main_state.planningModule)
        self.clothes_detector_perception = ClothesDetectorPerception(main_state.planningModule)
        self.leg_people = PeopleLegDetection(main_state.planningModule)