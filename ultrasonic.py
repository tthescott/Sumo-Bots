# bot drives forward until it gets close to something,
# then turns around and repeats

import time
import signal
from robot_controller import Robot

# initiate robot object
bot = Robot()
bot.sonic_up()

# global variables
run = True
speed = 100
stop_distance = 300 # mm
turn_duration = 0.3 # seconds

# handles stopping the program
def stop_execution(sig, frame):
  global run
  print("\nRun stop.py if the robot didn't stop")
  run = False

# invoke stop_execution on Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, stop_execution)

# main loop
try:
  while run:
    bot.drive_forward_forever(speed)

    # measure distance continuously
    if bot.get_distance() <= stop_distance:
      # stop and turn away
      bot.stop_motors()
      bot.turn_right(speed, turn_duration)

finally:
  # stop motors and ultrasonic
  bot.stop_motors()
  bot.sonic_down()
