import sys

sys.path.append('/usr/local/lib/python3.11/dist-packages')

import time
from Raspbot_Lib import Raspbot

bot = Raspbot()
speed = 60  # Keep this constant for all tests
stop_distance = 200 # in mm
duration = 2.0 # Seconds

# ultra sonic
bot.Ctrl_Ulatist_Switch(1) #open
time.sleep(1)

def get_distance():
    diss_H =bot.read_data_array(0x1b,1)[0]
    diss_L =bot.read_data_array(0x1a,1)[0]
    dis = diss_H<< 8 | diss_L
    print(str(dis) + "mm")
    return dis

def drive_forward():
    bot.Ctrl_Muto(0, speed)
    bot.Ctrl_Muto(1, speed)
    bot.Ctrl_Muto(2, speed)
    bot.Ctrl_Muto(3, speed)

def turn():
    bot.Ctrl_Muto(0, speed)
    bot.Ctrl_Muto(1, speed)
    bot.Ctrl_Muto(2, -speed)
    bot.Ctrl_Muto(3, -speed)

def stop_motors():
    bot.Ctrl_Muto(0, 0)
    bot.Ctrl_Muto(1, 0)
    bot.Ctrl_Muto(2, 0)
    bot.Ctrl_Muto(3, 0)


try:
    while True:
        print("1")
        drive_forward()
        print("2")
        distance = get_distance()

        if distance <= stop_distance:
            print("I AM TURNING")
            stop_motors()
            turn()
            time.sleep(.9)
            stop_motors()

except KeyboardInterrupt:
    stop_motors()
    bot.Ctrl_Ulatist_Switch(0) #close
    print("Motors stopped")
