__author__ = 'Nicole'


class NeckStatus:
    def __init__(self):
        pass

    neckStatus = {
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
        return NeckStatus.neckStatus[int(status)]

if __name__ == "__main__":
    print NeckStatus.get_state_from_status(4)