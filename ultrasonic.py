# bot drives forward until it gets close to something,
# then turns around and repeats

import time
import signal
import random
from robot_controller import Robot

# set up robot, ultrasonic, and execution loop stop
bot = Robot()
bot.sonic_up()
signal.signal(signal.SIGINT, bot.stop_execution)

# global variables
speed = 50
stop_distance = 300 # mm
turn_duration = 0.5 # seconds

# main loop
try:
  while bot.is_running():
    bot.drive_forward_forever(speed)
    # measure distance every .1 seconds
    time.sleep(.1)
    if bot.get_distance() <= stop_distance:
      # stop and turn left or right
      bot.stop_motors()
      if random.randint(0, 1) == 0:
        bot.turn_right_time(speed, turn_duration)
      else:
        bot.turn_left_time(speed, turn_duration)

finally:
  # stop motors and ultrasonic
  bot.stop_motors()
  bot.sonic_down()
