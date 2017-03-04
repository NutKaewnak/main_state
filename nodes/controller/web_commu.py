import rospy
import paho.mqtt.client as mqtt
import json

__author__ = 'cin'

broker = "fptrainnie"
port = 1883


class WebCommu:
    def __init__(self):
        self.client= mqtt.Client()
        self.client.connect(broker, port)

    def set_data(self, status, table, order):
        data = {'name': 'lumyai', 'status': status, 'table': table, 'order': order}
        self.on_publish(data)

    def on_publish(self, data):
        self.client.public("/ROBOT", json.dumps(data))
