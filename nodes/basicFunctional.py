__author__ = 'nicole'
from include.base_state import *
from factory.move import Move
from factory.neck import Neck


class BasicFunctionality(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.object = None

    def main(self, device, data):
        if self.state is STATE.INIT:
            Move.toLocation().to('pick&place')
            self.changeStateTo('moveToPick&Place')

        elif self.state is 'moveToPick&Place':
            if Move.toLocation().state is STATE.SUCCEED:
                # recognize both object
                # Grab.normal().grab(self.object)
                self.changeStateTo(STATE.GRAB)

        elif self.state is STATE.GRAB and self.object.isKnown is True:
            # if Grab.normal().state is STATE.SUCCESS:
                # Grab.place().at(self.object.location)
                self.changeStateTo(STATE.PLACE)
        elif self.state is STATE.GRAB and self.object.isKnown is False:
            # if Grab.normal().state is STATE.SUCCEED:
                # Grab.place().at('bin')
                self.changeStateTo(STATE.PLACE)

        elif self.state is STATE.PLACE:
            # if Grab.place().state is STATE.SUCCEED:
                Move.toLocation().to('Final')
                self.changeStateTo('final')

        elif self.state is 'final':
            if Move.toLocation().state is STATE.SUCEED:
                # Move.follow().person(Kinnect.getPeople().find())
                self.changeStateTo(STATE.DETECT)

        elif self.state is STATE.DETECT:
            # answer random question
            # if done:
                Move.toLocation().to('exit')
                self.changeStateTo(STATE.EXIT)

        elif self.state is STATE.EXIT:
            if Move.toLocation().state is STATE.SUCCEED:
                # say I will now stop
                self.changeStateTo(STATE.SUCCEED)
if __name__ == '__main__':
    BaseState()