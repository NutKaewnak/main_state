__author__ = 'antonio'
from include.publish import Publish
class NeckTurn:
    @staticmethod
    def turn(angle):
        Publish.set_neck(0, 0, angle)