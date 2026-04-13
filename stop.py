import sys

sys.path.append('/usr/local/lib/python3.11/dist-packages')

import time
from Raspbot_Lib import Raspbot

bot = Raspbot()
speed = 30  # Keep this constant for all tests
stop_distance = 100 # in mm
duration = 2.0 # Seconds

def stop_motors():
    bot.Ctrl_Muto(0, 0)
    bot.Ctrl_Muto(1, 0)
    bot.Ctrl_Muto(2, 0)
    bot.Ctrl_Muto(3, 0)

stop_motors()
