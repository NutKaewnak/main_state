__author__ = "AThousandYears"
import rospy
from std_msgs.msg import String, Int64
from skill.skill_book import SkillBook
from subtask.subtask_book import SubtaskBook
from task.task_book import TaskBook

class PlanningModule:

    def __init__(self, main_state):
        self.task = main_state.task
        self.perceptionModule = None

        self.skillBook = SkillBook(main_state.controlModule)
        self.subtaskBook = SubtaskBook(self)
        self.subtaskBook.set_subtask_book(self)
        self.taskBook = TaskBook(self)

        # rospy.init_node('~current')
        self.pub_state = rospy.Publisher('~state', String, queue_size=1)
        self.pub_running = rospy.Publisher('~running', Int64, queue_size=1)
        self.running = 0

    def set_perception(self, perception_module):
        self.skillBook.set_perception(perception_module)
        self.subtaskBook.set_perception(perception_module)
        self.taskBook.set_perception(perception_module)

        self.perceptionModule = perception_module

    def perform(self, perception_data):
        if self.perceptionModule is not None:
            if self.perceptionModule.delay.is_waiting():
                return
        # print perception_data
        self.running = self.running + 1
        self.pub_state.publish(String(self.taskBook.book[self.task].state))
        self.pub_running.publish(Int64(self.running))
        self.taskBook.book[self.task].act(perception_data)
        self.running = self.running - 1
