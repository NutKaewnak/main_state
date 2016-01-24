from people_detect import PeopleDetect
from move_pass_door import MovePassDoor
from move_to_location import MoveToLocation
from register import Register
from introduce import Introduce
from leave_arena import LeaveArena
from find_people_and_get_order import FindPeopleAndGetOrder
from detect_and_move_to_people import DetectAndMoveToPeople
from follow_person import FollowPerson
from move_relative import MoveRelative
from bring_object_to_person import BringObjectToPerson
from question_answer import QuestionAnswer
from move_absolute import MoveAbsolute
from say import Say
from pick import Pick
from detect_waving_people import DetectWavingPeople
from search_waving_people import SearchWavingPeople
from detect_front_person import DetectFrontPerson
# from object_recognition_subtask import ObjectRecognition
from set_height_relative import SetHeightRelative
from scissor_rock_paper import ScissorRockPaper
from recognize_objects import RecognizeObjects
from test_subtask_skill import TestSubtaskSkill

__author__ = "AThousandYears"


class SubtaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['PeopleDetect'] = PeopleDetect(planning_module)
        self.book['MovePassDoor'] = MovePassDoor(planning_module)
        self.book['MoveToLocation'] = MoveToLocation(planning_module)
        self.book['Introduce'] = Introduce(planning_module)
        self.book['Register'] = Register(planning_module)
        self.book['LeaveArena'] = LeaveArena(planning_module)
        self.book['FindPeopleAndGetOrder'] = FindPeopleAndGetOrder(planning_module)
        self.book['DetectAndMoveToPeople'] = DetectAndMoveToPeople(planning_module)
        self.book['FollowPerson'] = FollowPerson(planning_module)
        self.book['MoveRelative'] = MoveRelative(planning_module)
        self.book['BringObjectToPerson'] = BringObjectToPerson(planning_module)
        self.book['QuestionAnswer'] = QuestionAnswer(planning_module)
        self.book['MoveAbsolute'] = MoveAbsolute(planning_module)
        self.book['Say'] = Say(planning_module)
        self.book['Pick'] = Pick(planning_module)
        self.book['DetectWavingPeople'] = DetectWavingPeople(planning_module)
        self.book['SearchWavingPeople'] = SearchWavingPeople(planning_module)
        self.book['DetectFrontPerson'] = DetectFrontPerson(planning_module)
        # self.book['ObjectRecognition'] = ObjectRecognition(planning_module)
        self.book['SetHeightRelative'] = SetHeightRelative(planning_module)
        self.book['ScissorRockPaper'] = ScissorRockPaper(planning_module)
        self.book['RecognizeObjects'] = RecognizeObjects(planning_module)
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
