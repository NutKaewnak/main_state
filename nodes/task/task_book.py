from basic_functional import BasicFunctional
from cocktail import Cocktail
from rips import RIPS
from test import Test
from follow_me import FollowMe
from testSpeech import TestSpeech
from restaurant import Restaurant
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
from test_object3ds_detection import TestObject3DsDetection
from restaurant_vdo import RestaurantVDO
from test_neck import TestNeck
from restaurant_Frank import RestaurantFrank
from test_bug_arm import TestBugArm

__author__ = "AThousandYears"


class TaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['RIPS'] = RIPS(planning_module)
        self.book['Test'] = Test(planning_module)
        self.book['BasicFunctional'] = BasicFunctional(planning_module)
        self.book['Cocktail'] = Cocktail(planning_module)
        self.book['FollowMe'] = FollowMe(planning_module)
        self.book['TestSpeech'] = TestSpeech(planning_module)
        self.book['Restaurant'] = Restaurant(planning_module)
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
        self.book['RecognitionTesting'] = TestRecognition(planning_module)
        self.book['TestObject3DsDetection'] = TestObject3DsDetection(planning_module)
        self.book['RestaurantVDO'] = RestaurantVDO(planning_module)
        self.book['TestNeck'] = TestNeck(planning_module)
        self.book['RestaurantFrank'] = RestaurantFrank(planning_module)
        self.book['TestBugArm'] = TestBugArm(planning_module)

    def set_perception(self, perception_module):
        for task in self.book:
            self.book[task].set_perception(perception_module)
