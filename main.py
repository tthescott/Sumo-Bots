import signal
import random
import time
from robot_controller import Robot

# initiate robot object
bot = Robot()
bot.sonic_up()
signal.signal(signal.SIGINT, bot.stop_execution)

# global variables
cruise_speed = 60
attack_speed = 160
stop_distance = 300 # mm
turn_duration = 0.3 # seconds

# migrate to robot_controller later
def turn_left_until_find(bot, speed, angle):
  while True:
    # bot.turn_left_degrees(cruise_speed, 15)
    bot.turn_left(cruise_speed, .1)
    time.sleep(.1)
    if bot.get_distance() <= stop_distance:
      return

# main loop
try:
  # drive to black line (simulated for now)
  bot.drive_forward_timed(cruise_speed, 2)

  while bot.is_running():
    # scan for enemy
    turn_left_until_find(bot, cruise_speed, 10)

    # attack them (tape simulated by time for now)
    time.sleep(.1)
    bot.drive_forward_timed(attack_speed, 2)

finally:
  # stop motors and ultrasonic
  bot.stop_motors()
  bot.sonic_down()
