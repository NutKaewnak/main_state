__author__ = 'nicole'
import rospy

class TestDataPath:
    def __init__(self):
        rospy.wait_for_service('add_two_ints')
        try:
            add_two_ints = rospy.ServiceProxy('add_two_ints', MockObject)
            resp1 = add_two_ints(x, y)
            return resp1.sum
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    def usage():
        return "%s [x y]"%sys.argv[0]

