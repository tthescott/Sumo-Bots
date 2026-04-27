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
cruise_speed = 50
turn_speed = 10
attack_speed = 100
attack_distance = 400 # mm

# main loop
try:
  time.sleep(.1)

  # drive to black line (simulated for now)
  bot.drive_forward_timed(cruise_speed, 2)

  while bot.is_running():
    # scan for enemy
    bot.scan_left(turn_speed, attack_distance)

    # attack them (tape simulated by time for now)
    bot.attack(attack_speed, 2)

finally:
  bot.stop_motors()
  bot.sonic_down()
  bot.LED_off()
