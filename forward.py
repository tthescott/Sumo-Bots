import time
import signal
from robot_controller import Robot

# initialize robot object
bot = Robot()

# Ctrl+C stops execution
signal.signal(signal.SIGINT, bot.stop_execution)

# globals
speed = 160

# main loop
try:
  bot.drive_forward_forever(speed)
  while bot.is_running():
    bot.turn_on_lights(1, 0)
    time.sleep(1)
    bot.turn_on_lights(1, 1)
    time.sleep(1)
    bot.turn_on_lights(1, 2)
    time.sleep(1)

finally:
  # stop motors and ultrasonic
  bot.stop_motors()
  bot.sonic_down()
  bot.turn_on_lights(0, 0)
