import time
import signal
from robot_controller import Robot

# set up bot and Ctrl+C to stop main loop
bot = Robot()
signal.signal(signal.SIGINT, bot.stop_execution)

# global variables
speed = 30

# main execution loop
try:
  bot.drive_forward_forever(speed)
  while bot.is_running():
    time.sleep(.05)

    # read all four light sensors
    track = bot.read_data_array()
    track = int(track[0])
    x1 = (track>>3)&0x01
    x2 = (track>>2)&0x01
    x3 = (track>>1)&0x01
    x4 = (track)&0x01

    print(track, x1, x2, x3, x4)
    sum = x1 + x2 + x3 + x4

    # stop when any sensor reads black
    if sum < 4:
      bot.stop_motors()
      break

finally:
  bot.stop_motors()
