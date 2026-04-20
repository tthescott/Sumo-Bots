import signal
import random
import time
from robot_controller import Robot

# initialize robot object
bot = Robot()
bot.sonic_up()

# Ctrl+C stops execution
signal.signal(signal.SIGINT, bot.stop_execution)

# global variables
cruise_speed = 60
attack_speed = 160
attack_distance = 300 # mm
turn_duration = 0.3 # seconds

# main loop
try:
  # drive to black line (simulated for now)
  bot.drive_forward_timed(cruise_speed, 2)

  while bot.is_running():
    # scan for enemy
    bot.scan_left(cruise_speed, turn_duration, attack_distance)

    # attack them (tape simulated by time for now)
    bot.drive_forward_timed(attack_speed, 2)

finally:
  # stop motors and ultrasonic
  bot.stop_motors()
  bot.sonic_down()
