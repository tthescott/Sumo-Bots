# drive forward until it hits a black line, then stop

import time
import signal
from robot_controller import Robot

# set up robot and execution loop stop
bot = Robot()
signal.signal(signal.SIGINT, bot.stop_execution)

# global variables
speed = 30

# main execution loop
try:
  bot.drive_forward_forever(speed)
  while bot.is_running():
    # read light sensors every .05 seconds
    time.sleep(.05)
    data = bot.read_data_array()
    x1 = (data>>3)&0x01
    x2 = (data>>2)&0x01
    x3 = (data>>1)&0x01
    x4 = (data)&0x01

    print(data, x1, x2, x3, x4)
    sum = x1 + x2 + x3 + x4

    # stop when any sensor reads black
    if sum < 4:
      bot.stop_motors()
      break

finally:
  bot.stop_motors()
