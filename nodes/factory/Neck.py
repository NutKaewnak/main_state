from skill.neckLookDown import neckLookDown

__author__ = 'nicole'
class Neck:
    lookdown = None
    def __init__(self):
        pass

    @staticmethod
    def lookDown():
        if Neck.lookdown is None:
            Neck.lookdown = neckLookDown()
        return Neck.lookdown

