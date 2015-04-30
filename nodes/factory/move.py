from skill.moveRelative import moveRelative
from skill.moveToLocation import moveToLocation
from subtask.MovePassDoor import MovePassDoor
from subtask.followPerson import FollowPerson

__author__ = 'nicole'


class Move():
    movePassDoor = None
    moveToLocation = None
    moveRelative = None
    followPerson = None
    def __init__(self):
        pass

    @staticmethod
    def passDoor():
        if Move.movePassDoor is None:
            Move.movePassDoor = MovePassDoor()
        return Move.movePassDoor

    @staticmethod
    def relative():
        if Move.moveRelative is None:
            Move.moveRelative = moveRelative()
        return moveRelative

    @staticmethod
    def toLocation():
        if Move.moveToLocation is None:
            Move.moveToLocation = moveToLocation()
        return Move.moveToLocation

    @staticmethod
    def follow():
        if Move.followPerson is None:
            Move.followPerson = FollowPerson()
        return Move.followPerson
