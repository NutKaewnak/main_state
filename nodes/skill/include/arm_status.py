__author__ = 'Nicole'


class ArmStatus:
    def __init__(self):
        pass

    armStatus = {
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
        return ArmStatus.armStatus[int(status)]

if __name__ == "__main__":
    print ArmStatus.get_state_from_status(4)