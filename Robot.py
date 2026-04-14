import sys
import time

# tell python where Raspbot_Lib is
sys.path.append('/usr/local/lib/python3.11/dist-packages')
from Raspbot_Lib import Raspbot

class Robot():

  # initialize raspbot object
  def __init__(self):
    self.raspbot = Raspbot()
  
  #------------- movement -------------

  # drive forward with no stop
  def drive_forward_forever(self, speed):
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)

  # drive backward with no stop
  def drive_backward_forever(self, speed):
    self.raspbot.Ctrl_Muto(0, -speed)
    self.raspbot.Ctrl_Muto(1, -speed)
    self.raspbot.Ctrl_Muto(2, -speed)
    self.raspbot.Ctrl_Muto(3, -speed)

  # drive forward for a duration of time
  def drive_forward_timed(self, speed, duration):
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    time.sleep(duration)
    self.stop_motors()
  
  # drive backward for a duration of time
  def drive_backward_timed(self, speed, duration):
    self.raspbot.Ctrl_Muto(0, -speed)
    self.raspbot.Ctrl_Muto(1, -speed)
    self.raspbot.Ctrl_Muto(2, -speed)
    self.raspbot.Ctrl_Muto(3, -speed)
    time.sleep(duration)
    self.stop_motors()

  # stop all wheel motors
  def stop_motors(self):
    self.raspbot.Ctrl_Muto(0, 0)
    self.raspbot.Ctrl_Muto(1, 0)
    self.raspbot.Ctrl_Muto(2, 0)
    self.raspbot.Ctrl_Muto(3, 0)

  # turn right for a duration of time
  def turn_right(self, speed, duration):
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, -speed)
    self.raspbot.Ctrl_Muto(3, -speed)
    time.sleep(duration)
    self.stop_motors()

  # turn left for a duration of time
  def turn_left(self, speed, duration):
    self.raspbot.Ctrl_Muto(0, -speed)
    self.raspbot.Ctrl_Muto(1, -speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    time.sleep(duration)
    self.stop_motors()

  #------------- ultrasonic -------------

  # activate ultrasonic sensor
  def sonic_up(self):
    self.raspbot.Ctrl_Ulatist_Switch(1)
    # give time to calibrate
    time.sleep(1)

  # deactivate ultrasonic sensor
  def sonic_down(self):
    self.raspbot.Ctrl_Ulatist_Switch(0)

  # measure distance in mm with ultrasonic sensor
  def get_distance(self):
    diss_H = self.raspbot.read_data_array(0x1b,1)[0]
    diss_L = self.raspbot.read_data_array(0x1a,1)[0]
    dis = diss_H<< 8 | diss_L
    return dis
