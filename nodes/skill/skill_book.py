from move_base_absolute import MoveBaseAbsolute
from move_base_relative import MoveBaseRelative
from move_base_relative_twist import MoveBaseRelativeTwist
from rips_out import RipsOut
from say import Say
from confirm import Confirm
from turn_neck import TurnNeck
from set_height_relative import SetHeightRelative
from count import Count
from grasp import Grasp
from recognize_objects import RecognizeObjects
from detect_object_3ds import DetectObject3Ds
from voice_recognition_mode import VoiceRecognitionMode
from arm_static_pose import ArmStaticPose
from detect_clothes import DetectClothes
from play_sound import PlaySound
from web_commu import WebCommu
__author__ = "AThousandYears"


class SkillBook:
    def __init__(self, control_module):
        self.book = dict()
        self.book['MoveBaseAbsolute'] = MoveBaseAbsolute(control_module)
        self.book['MoveBaseRelative'] = MoveBaseRelative(control_module)
        self.book['MoveBaseRelativeTwist'] = MoveBaseRelativeTwist(control_module)
        self.book['RipsOut'] = RipsOut(control_module)
        self.book['Say'] = Say(control_module)
        self.book['Confirm'] = Confirm(control_module)
        self.book['TurnNeck'] = TurnNeck(control_module)
        self.book['SetHeightRelative'] = SetHeightRelative(control_module)
        self.book['Count'] = Count(control_module)
        self.book['Grasp'] = Grasp(control_module)
        self.book['RecognizeObjects'] = RecognizeObjects(control_module)
        self.book['DetectObject3Ds'] = DetectObject3Ds(control_module)
        self.book['VoiceRecognitionMode'] = VoiceRecognitionMode(control_module)
        self.book['ArmStaticPose'] = ArmStaticPose(control_module)
        self.book['DetectClothes'] = DetectClothes(control_module)
        self.book['PlaySound'] = PlaySound(control_module)
        self.book['WebCommu'] = WebCommu(control_module)

    def get_skill(self, subtask, skill_name):
        self.book[skill_name].reset()
        subtask.current_skill = self.book[skill_name]
        return self.book[skill_name]

    def set_perception(self, perception_module):
        for skill in self.book:
            self.book[skill].set_perception(perception_module)
