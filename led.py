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
  while bot.is_running():
    bot.LED_on("red")
    time.sleep(1)
    bot.LED_on("green")
    time.sleep(1)
    bot.LED_on("blue")
    time.sleep(1)
    bot.LED_on("yellow")
    time.sleep(1)
    bot.LED_on("purple")
    time.sleep(1)
    bot.LED_on("cyan")
    time.sleep(1)
    bot.LED_on("white")
    time.sleep(1)
    bot.LED_on("violet")

finally:
  bot.stop_motors()
  bot.sonic_down()
  bot.LED_off()
