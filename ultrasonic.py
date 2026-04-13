import Robot

bot = Robot()
bot.sonic_up()

speed = 60
stop_distance = 200 # mm
duration = 0.9 # seconds

try:
    while True:
        bot.drive_forward(speed)

        if bot.get_distance() <= stop_distance:
            bot.stop_motors()
            bot.turn(speed, duration)

except KeyboardInterrupt:
    bot.stop_motors()
    bot.sonic_down()
