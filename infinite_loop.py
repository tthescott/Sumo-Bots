# !!! not functional !!!

from robot_controller import Robot

bot = Robot()
speed = 80

while True:
    track = bot.read_data_array(0x0a, 1) # won't work, haven't made function
    track = int(track[0])
    x1 = (track>>3)&0x01
    x2 = (track>>2)&0x01
    x3 = (track>>1)&0x01
    x4 = (track)&0x01
    print(track, x1, x2, x3, x4)

    # if x1 and x2 and x3 and x4:
      # bot.stop_motors()
      # break

    #bot.drive_forward(speed)
