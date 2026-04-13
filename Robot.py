import sys 
import time

# tell python where Raspbot_Lib is
sys.path.append('/usr/local/lib/python3.11/dist-packages')
from Raspbot_Lib import Raspbot

class Robot():

  def __init__(self):
    self.raspbot = Raspbot()
  
  #------------- movement -------------

  def drive_forward(self, speed):
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    print("driving forward")

  def stop_motors(self):
    self.raspbot.Ctrl_Muto(0, 0)
    self.raspbot.Ctrl_Muto(1, 0)
    self.raspbot.Ctrl_Muto(2, 0)
    self.raspbot.Ctrl_Muto(3, 0)
    print("stopped motors")

  def turn(self, speed, duration):
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, -speed)
    self.raspbot.Ctrl_Muto(3, -speed)
    time.sleep(duration)
    self.stop_motors()
    print(f"turned at {speed} speed for {duration} seconds")

  #------------- ultrasonic -------------

  def sonic_up(self):
    # set up ultra sonic sensor
    self.raspbot.Ctrl_Ulatist_Switch(1)
    print("sonic up")

  def sonic_down(self):
    # shut down ultra sonic sensor
    self.raspbot.Ctrl_Ulatist_Switch(0)
    print("sonic down")

  def get_distance(self):
    diss_H = self.raspbot.read_data_array(0x1b,1)[0]
    diss_L = self.raspbot.read_data_array(0x1a,1)[0]
    dis = diss_H<< 8 | diss_L
    return dis
