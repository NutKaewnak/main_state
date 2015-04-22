__author__ = "AThousandYears"

from perception.include.abstract_perception import AbstractPerception
from perception.include.devices import Devices
from perception.base_status import BaseStatusPerception
from perception.voice import VoicePerception


class PerceptionModule:

    def __init__(self, main_state):
        self.Devices = Devices
        self.base_status = BaseStatusPerception(main_state.planningModule)
        self.base_position = AbstractPerception(main_state.planningModule)
        self.voice = VoicePerception(main_state.planningModule)

