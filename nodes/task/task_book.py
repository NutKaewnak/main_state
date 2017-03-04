from basic_functional import BasicFunctional
from cocktail import Cocktail
from rips import RIPS
from follow_me import FollowMe
from restaurant import Restaurant
from GPSR import GPSR
from speech_recognition import SpeechRecognition
from manipulation_task import ManipulationTask
from navigation_task import NavigationTask
from inspection import Inspection
from robozoo import RoboZoo
from robo_nurse import RoboNurse
from today_show import TodayShow
from restaurant_vdo import RestaurantVDO
from restaurant_Frank import RestaurantFrank
from separate_clothes_op import SeparateClothesOP
from follow_guiding import FollowGuiding

from test import Test
from testSpeech import TestSpeech
from test_object_recog_and_manip import TestObjectRecogAndManip
from test_detect_and_move_to_person import TestDetectAndMoveToPerson
from recognition_testing import TestRecognition
from test_object3ds_detection import TestObject3DsDetection
from test_neck import TestNeck
from test_pill import TestPill
from test_detect_object import TestDetectObject
from test_follow_leg import TestFollowLeg
from EEGPSR import EEGPSR
from test_move import TestMove
from joy_state import JoyState
from cp_answer_and_read_qr import CPAnswerAndReadQR
from cp_walk_open import CPWalkOpen
from restaurant_cin import RestaurantCin
__author__ = "AThousandYears"


class TaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['RIPS'] = RIPS(planning_module)
        self.book['BasicFunctional'] = BasicFunctional(planning_module)
        self.book['Cocktail'] = Cocktail(planning_module)
        self.book['FollowMe'] = FollowMe(planning_module)
        self.book['Restaurant'] = Restaurant(planning_module)
        self.book['GPSR'] = GPSR(planning_module)
        self.book['SpeechRecognition'] = SpeechRecognition(planning_module)
        self.book['ManipulationTask'] = ManipulationTask(planning_module)
        self.book['NavigationTask'] = NavigationTask(planning_module)
        self.book['Inspection'] = Inspection(planning_module)
        self.book['RoboZoo'] = RoboZoo(planning_module)
        self.book['RoboNurse'] = RoboNurse(planning_module)
        self.book['TodayShow'] = TodayShow(planning_module)
        self.book['RestaurantVDO'] = RestaurantVDO(planning_module)
        self.book['RestaurantFrank'] = RestaurantFrank(planning_module)
        self.book['SeparateClothesOP'] = SeparateClothesOP(planning_module)
        self.book['FollowGuiding'] = FollowGuiding(planning_module)

        self.book['Test'] = Test(planning_module)
        self.book['TestSpeech'] = TestSpeech(planning_module)
        self.book['TestObjectRecogAndManip'] = TestObjectRecogAndManip(planning_module)
        self.book['TestDetectAndMoveToPerson'] = TestDetectAndMoveToPerson(planning_module)
        self.book['RecognitionTesting'] = TestRecognition(planning_module)
        self.book['TestObject3DsDetection'] = TestObject3DsDetection(planning_module)
        self.book['TestNeck'] = TestNeck(planning_module)
        self.book['TestPill'] = TestPill(planning_module)
        self.book['TestDetectObject'] = TestDetectObject(planning_module)
        self.book['TestFollowLeg'] = TestFollowLeg(planning_module)
        self.book['EEGPSR'] = EEGPSR(planning_module)
        self.book['TestMove'] = TestMove(planning_module)
        self.book['JoyState'] = JoyState(planning_module)
        self.book['CPAnswerAndReadQR'] = CPAnswerAndReadQR(planning_module)
        self.book['CPWalkOpen'] = CPWalkOpen(planning_module)
        self.book['RestaurantCin'] = RestaurantCin(planning_module)


    def set_perception(self, perception_module):
        for task in self.book:
            self.book[task].set_perception(perception_module)
