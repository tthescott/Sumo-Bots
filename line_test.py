import sys

sys.path.append('/usr/local/lib/python3.11/dist-packages')

import time
from Raspbot_Lib import Raspbot
bot = Raspbot()
speed = 10  # Keep this constant for all tests
# duration = 3.0 # Seconds

# print(f"Starting calibration: {speed} speed for {duration} seconds...")

def stop_motors():
    bot.Ctrl_Muto(0, 0)
    bot.Ctrl_Muto(1, 0)
    bot.Ctrl_Muto(2, 0)
    bot.Ctrl_Muto(3, 0)

def drive(speed_vel):
    # Drive forward
    bot.Ctrl_Muto(0, speed_vel)
    bot.Ctrl_Muto(1, speed_vel)
    bot.Ctrl_Muto(2, speed_vel)
    bot.Ctrl_Muto(3, speed_vel)


# black = 0
# white = 15
# while True:
#     track = bot.read_data_array(0x0a, 1)
#     track = int(track[0])
#     x1 = (track>>3)&0x01
#     x2 = (track>>2)&0x01
#     x3 = (track>>1)&0x01
#     x4 = (track)&0x01
#     print(track, x1, x2, x3, x4)

#     if track == black:
#        stop_motors()
#        break

#     drive(speed)


def turn_right_in_place(degree):
    speed = 10
    bot.Ctrl_Muto(0, speed)
    bot.Ctrl_Muto(1, speed*1.2)
    bot.Ctrl_Muto(2, -speed)
    bot.Ctrl_Muto(3, -speed)

    time.sleep(4.35 * degree / 360)

turn_right_in_place(180)
stop_motors()
# time.sleep(1.5)
# drive(-speed)
# time.sleep(1)
# stop_motors()
