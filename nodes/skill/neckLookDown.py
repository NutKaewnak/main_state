from math import pi
from include.publish import Publish

__author__ = 'nicole'

class neckLookDown:
    @staticmethod
    def lookDown():
        Publish.set_neck(0, 50*pi/180, 0)
