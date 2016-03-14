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
        return MoveBaseStatus.moveBaseStatus[int(status)]

    @staticmethod
    def is_active(status):
        return status in [0, 1, 6, 7]

if __name__ == "__main__":
    print MoveBaseStatus.get_state_from_status(4)
