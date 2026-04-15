import time
import signal
from robot_controller import Robot

run = True
speed = 30

bot = Robot()

# handles stopping the program
def stop_execution(sig, frame):
  global run
  print("\nRun stop.py if the robot didn't stop")
  run = False

# invoke stop_execution on Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, stop_execution)

try:
  bot.drive_forward_forever(speed)
  while run:
    time.sleep(.05)
    track = bot.read_data_array()
    track = int(track[0])
    x1 = (track>>3)&0x01
    x2 = (track>>2)&0x01
    x3 = (track>>1)&0x01
    x4 = (track)&0x01
    print(track, x1, x2, x3, x4)

    sum = x1 + x2 + x3 + x4

    # stop when any sensor reads black
    if sum <= 3:
      bot.stop_motors()
      break

finally:
  bot.stop_motors()
