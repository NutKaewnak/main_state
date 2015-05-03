__author__ = "AThousandYears"

from move_pass_door import MovePassDoor
from move_to_location import MoveToLocation
from register import Register
from introduce import Introduce
from leave_arena import LeaveArena
from find_people_and_get_order import FindPeopleAndGetOrder
from find_people_using_gesture import FindPeopleUsingGesture
from grab_object_to_person import GrabObjectToPerson
from detect_and_move_to_people import DetectAndMoveToPeople
from follow_person import FollowPerson
from grab import Grab
from move_relative import MoveRelative
from ask_for_name import AskForName
from ask_for_object import AskForObject
from ask_for_name_and_command import AskForNameAndCommand
from bring_object_to_person import BringObjectToPerson
from question_answer import QuestionAnswer
from find_people import FindPeople
from move_absolute import MoveAbsolute
from say import Say
from extract_object_location import ExtractObjectLocation


class SubtaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['FindPeople'] = FindPeople(planning_module)
        self.book['MovePassDoor'] = MovePassDoor(planning_module)
        self.book['MoveToLocation'] = MoveToLocation(planning_module)
        self.book['Introduce'] = Introduce(planning_module)
        self.book['Register'] = Register(planning_module)
        self.book['LeaveArena'] = LeaveArena(planning_module)
        self.book['FindPeopleAndGetOrder'] = FindPeopleAndGetOrder(planning_module)
        self.book['FindPeopleUsingGesture'] = FindPeopleUsingGesture(planning_module)
        self.book['GrabObjectToPerson'] = GrabObjectToPerson(planning_module)
        self.book['DetectAndMoveToPeople'] = DetectAndMoveToPeople(planning_module)
        self.book['FollowPerson'] = FollowPerson(planning_module)
        self.book['MoveRelative'] = MoveRelative(planning_module)
        self.book['Grab'] = Grab(planning_module)
        self.book['BringObjectToPerson'] = BringObjectToPerson(planning_module)
        self.book['AskForName'] = AskForName(planning_module)
        self.book['AskForObject'] = AskForObject(planning_module)
        self.book['AskForNameAndCommand'] = AskForNameAndCommand(planning_module)
        self.book['QuestionAnswer'] = QuestionAnswer(planning_module)
        self.book['MoveAbsolute'] = MoveAbsolute(planning_module)
        self.book['Say'] = Say(planning_module)
        self.book['ExtractObjectLocation'] = ExtractObjectLocation(planning_module)

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
