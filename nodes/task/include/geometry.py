from math import sqrt

class Geometry(object):

    @staticmethod
    def get_distance(point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

    # point_list must be dictionary
    @staticmethod
    def get_nearest_point(query_point, point_list):
        min_distance = 9999.0
        result_index = None
        for index in point_list:
            distance = Geometry.get_distance(query_point, point_list[index])
            if distance < min_distance:
                min_distance = distance
                result_index = index
        return result_index


if __name__ == "__main__":
    print "Test case for Geometry class"

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    qp = Point(1.0,0.9)
    table_1 = Point(1.0,1.0)
    table_2 = Point(2.0,2.0)
    table_3 = Point(3.0,3.0)

    assert  Geometry.get_distance(table_1, table_2) == sqrt(2), "get_distance function error"
    assert  Geometry.get_distance(table_2, table_3) == sqrt(2), "get_distance function error"

    table_list = {'table_1' : table_1, 'table_2' : table_2, 'table_3' : table_3}
    assert Geometry.get_nearest_point(qp, table_list) == "table_1", "get_nearest_point function error"

    qp = Point(4.0,4.0)
    assert Geometry.get_nearest_point(qp, table_list) == "table_3", "get_nearest_point function error"
            
