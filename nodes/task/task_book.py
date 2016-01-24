__author__ = "AThousandYears"
from basic_functional import BasicFunctional
from cocktail import Cocktail
from rips import RIPS
from test import Test
from follow_me import FollowMe
from testSpeech import TestSpeach
from restaurant import Restaurant
# from test_gesture import TestGesture
from GPSR import GPSR
from speech_recognition import SpeechRecognition
from test_object_recog_and_manip import TestObjectRecogAndManip
from manipulation_task import ManipulationTask
from navigation_task import NavigationTask
from test_detect_and_move_to_person import TestDetectAndMoveToPerson
from inspection import Inspection
from robozoo import RoboZoo
from robo_nurse import RoboNurse
from today_show import TodayShow
from recognition_testing import TestRecognition
from test import Test


class TaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['RIPS'] = RIPS(planning_module)
        self.book['Test'] = Test(planning_module)
        self.book['BasicFunctional'] = BasicFunctional(planning_module)
        self.book['Cocktail'] = Cocktail(planning_module)
        self.book['FollowMe'] = FollowMe(planning_module)
        self.book['TestSpeach'] = TestSpeach(planning_module)
        self.book['Restaurant'] = Restaurant(planning_module)
        # self.book['TestGesture'] = TestGesture(planning_module)
        self.book['GPSR'] = GPSR(planning_module)
        self.book['SpeechRecognition'] = SpeechRecognition(planning_module)
        self.book['TestObjectRecogAndManip'] = TestObjectRecogAndManip(planning_module)
        self.book['ManipulationTask'] = ManipulationTask(planning_module)
        self.book['NavigationTask'] = NavigationTask(planning_module)
        self.book['TestDetectAndMoveToPerson'] = TestDetectAndMoveToPerson(planning_module)
        self.book['Inspection'] = Inspection(planning_module)
        self.book['RoboZoo'] = RoboZoo(planning_module)
        self.book['RoboNurse'] = RoboNurse(planning_module)
        self.book['TodayShow'] = TodayShow(planning_module)
        self.book['Test'] = Test(planning_module)
        self.book['RecognitionTesting'] =TestRecognition(planning_module)

    def set_perception(self, perception_module):
        for task in self.book:
            self.book[task].set_perception(perception_module)
