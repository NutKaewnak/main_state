from skill.moveRelative import moveRelative
from skill import moveToLocation
from subtask.MovePassDoor import MovePassDoor

__author__ = 'nicole'


class Move():
    movePassDoor = None
    moveToLocation = None
    def __init__(self):


    @staticmethod
    def passDoor():
        if Move.movePassDoor is None:
            Move.movePassDoor = MovePassDoor()
        return Move.movePassDoor

    @staticmethod
    def relative(x, y, z):
        return moveRelative(x, y, z)

    @staticmethod
    def toLocation(location):
        if Move.moveToLocation is None:
            Move.moveToLocation = moveToLocation()
        return Move.moveToLocation.toLocation(location)

5