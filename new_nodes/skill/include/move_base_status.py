__author__ = "AThousandYears"


class MoveBaseStatus:
    def __init__(self):
        pass

    moveBaseStatus = {
        0: 'pending',
        1: 'active',
        2: 'preempted',
        3: 'succeeded',
        4: 'aborted',
        5: 'rejected',
        6: 'preempting',
        7: 'recalling',
        8: 'recalled',
        9: 'lost'
    }

    @staticmethod
    def get_state_from_status(status):
        return MoveBaseStatus.moveBaseStatus[status]
