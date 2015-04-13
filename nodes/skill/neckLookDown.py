from math import pi
from include import publish

__author__ = 'nicole'

class neckLookDown:
    def __init__(self):
        publish.set_neck(0, 50*pi/180, 0)

if __name__ == '__main__':
    neckLookDown()