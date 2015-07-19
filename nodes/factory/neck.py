from skill.neckLookDown import NeckLookDown
from skill.neckStraight import NeckStraight
from skill.neckTurn import NeckTurn

__author__ = 'nicole'
class Neck:
    def __init__(self):
        pass

    @staticmethod
    def lookDown():
        NeckLookDown.lookDown()

    @staticmethod
    def lookStraigth():
        NeckStraight.NeckStraigth()

    @staticmethod
    def turn(angle):
        NeckTurn.turn(angle)
