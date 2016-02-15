#!/usr/bin/env python

import time
from controller.manipulator_controller import ManipulateController


mnplctrl = ManipulateController()
mnplctrl.init_controller()
mnplctrl.static_pose('right_arm', 'right_normal')
mnplctrl.static_pose('right_arm', 'right_push_chair_prepare')
time.sleep(5)
mnplctrl.static_pose('right_arm', 'right_push_chair_push')