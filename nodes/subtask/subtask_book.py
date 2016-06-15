from move_pass_door import MovePassDoor
from move_relative import MoveRelative
from move_to_location import MoveToLocation
from turn_neck import TurnNeck
from say import Say
from arm_static_pose import ArmStaticPose
from people_detect import PeopleDetect
from detect_door import DetectDoor
from detect_phone import DetectPhone
from detect_blanket import DetectBlanket
from detect_cane import DetectCane
from detect_middle_object import DetectMiddleObject
from pick import Pick
from follow_person import FollowPerson
from follow_me import FollowMe
from register import Register
from introduce import Introduce
from leave_arena import LeaveArena
from find_people_and_get_order import FindPeopleAndGetOrder
from detect_and_move_to_people import DetectAndMoveToPeople
from bring_object_to_person import BringGrabbingObjectToPerson
from question_answer import QuestionAnswer
from move_absolute import MoveAbsolute
from detect_waving_people import DetectWavingPeople
from search_waving_people import SearchWavingPeople
from detect_front_person import DetectFrontPerson
from set_height_relative import SetHeightRelative
from scissor_rock_paper import ScissorRockPaper
from recognize_objects import RecognizeObjects
from objects_detection import ObjectsDetection
from pills_detection import PillsDetection
from voice_recognition_mode import VoiceRecognitionMode
from find_cloth import FindCloth
from follow_leg import FollowLeg

from test_subtask_skill import TestSubtaskSkill

__author__ = "AThousandYears"


class SubtaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['MovePassDoor'] = MovePassDoor(planning_module)
        self.book['MoveRelative'] = MoveRelative(planning_module)
        self.book['MoveToLocation'] = MoveToLocation(planning_module)
        self.book['TurnNeck'] = TurnNeck(planning_module)
        self.book['Say'] = Say(planning_module)
        self.book['ArmStaticPose'] = ArmStaticPose(planning_module)
        self.book['PeopleDetect'] = PeopleDetect(planning_module)
        self.book['DetectDoor'] = DetectDoor(planning_module)
        self.book['DetectPhone'] = DetectPhone(planning_module)
        self.book['DetectBlanket'] = DetectBlanket(planning_module)
        self.book['DetectCane'] = DetectCane(planning_module)
        self.book['Introduce'] = Introduce(planning_module)
        self.book['Register'] = Register(planning_module)
        self.book['LeaveArena'] = LeaveArena(planning_module)
        self.book['FindPeopleAndGetOrder'] = FindPeopleAndGetOrder(planning_module)
        self.book['DetectAndMoveToPeople'] = DetectAndMoveToPeople(planning_module)
        self.book['FollowPerson'] = FollowPerson(planning_module)
        self.book['BringGrabbingObjectToPerson'] = BringGrabbingObjectToPerson(planning_module)
        self.book['QuestionAnswer'] = QuestionAnswer(planning_module)
        self.book['MoveAbsolute'] = MoveAbsolute(planning_module)
        self.book['Pick'] = Pick(planning_module)
        self.book['PillsDetection'] = PillsDetection(planning_module)
        self.book['DetectWavingPeople'] = DetectWavingPeople(planning_module)
        self.book['SearchWavingPeople'] = SearchWavingPeople(planning_module)
        self.book['DetectFrontPerson'] = DetectFrontPerson(planning_module)
        self.book['SetHeightRelative'] = SetHeightRelative(planning_module)
        self.book['ScissorRockPaper'] = ScissorRockPaper(planning_module)
        self.book['RecognizeObjects'] = RecognizeObjects(planning_module)
        self.book['ObjectsDetection'] = ObjectsDetection(planning_module)
        self.book['VoiceRecognitionMode'] = VoiceRecognitionMode(planning_module)
        self.book['FollowMe'] = FollowMe(planning_module)
        self.book['DetectMiddleObject'] = DetectMiddleObject(planning_module)
        self.book['FindCloth'] = FindCloth(planning_module)
        self.book['FollowLeg'] = FollowLeg(planning_module)

        self.book['TestSubtaskSkill'] = TestSubtaskSkill(planning_module)

    def get_subtask(self, task, subtask_name):
        self.book[subtask_name].reset()
        task.current_subtask = self.book[subtask_name]
        return self.book[subtask_name]

    def set_perception(self, perception_module):
        for subtask in self.book:
            self.book[subtask].set_perception(perception_module)

    def set_subtask_book(self, planning_module):
        for subtask in self.book:
            self.book[subtask].set_subtask_book(planning_module)
