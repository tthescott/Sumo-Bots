import signal
import random
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
attack_distance = 1000 # mm

# main loop
try:
  # drive to edge
  bot.drive_forward_forever(cruise_speed)

  # stop at edge
  while True:
    if bot.detect_tape():
      bot.stop_motors()
      break

  while bot.is_running():
    # go back a little bit
    bot.drive_backward_timed(cruise_speed, 1)

    # scan left or right for enemy
    if random.randint(0, 1) == 0:
      bot.scan_left(turn_speed, attack_distance)
    else:
      bot.scan_right(turn_speed, attack_distance)

    # attack them
    bot.attack(attack_speed, attack_distance)

finally:
  bot.stop_motors()
  bot.sonic_down()
  bot.LED_off()
