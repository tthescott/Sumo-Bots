import sys
import time
import bisect
import signal

# tell python where Raspbot_Lib is
sys.path.append('/usr/local/lib/python3.11/dist-packages')
from Raspbot_Lib import Raspbot

# ------------- turn calibration -------------

_RAW = {
  30:  [1.2162, 1.0465, 1.1111],
  60:  [0.6081, 0.6383],
  90:  [0.4762, 0.4839],
  120: [0.4186, 0.4018, 0.3965],
  150: [0.3689],
  180: [0.3383],
  210: [0.3147],
  255: [0.2961],
}

TURN_TABLE = {speed: sum(vals) / len(vals) for speed, vals in _RAW.items()}
_SPEEDS = sorted(TURN_TABLE.keys())

TURN_CORRECTION = 1.0  # increase if undershooting, decrease if overshooting

def turn_time(speed, angle=90):
  """Return duration in seconds to turn <angle> degrees at <speed>."""
  if angle == 0 or speed == 0:
    return 0.0
  spd = abs(speed)
  if spd <= _SPEEDS[0]:
    t90 = TURN_TABLE[_SPEEDS[0]]
  elif spd >= _SPEEDS[-1]:
    t90 = TURN_TABLE[_SPEEDS[-1]]
  else:
    i = bisect.bisect_right(_SPEEDS, spd) - 1
    lo, hi = _SPEEDS[i], _SPEEDS[i+1]
    t = (spd - lo) / (hi - lo)
    t90 = TURN_TABLE[lo] + t * (TURN_TABLE[hi] - TURN_TABLE[lo])
  return round(t90 * angle / 90 * TURN_CORRECTION, 4)

# --------------------------------------------

class Robot():

  def __init__(self):
    """Initialize raspbot object"""
    self.raspbot = Raspbot()
    self._run = True

    # for Ctrl+C from within a method (TODO: make functional)
    signal.signal(signal.SIGINT, self.stop_execution)

  # ------------- LEDs -------------

  def LED_on(self, color:str):
    """Turn on LEDs to given color\n
    Possible values: red, green, blue, yellow, purple, cyan, white"""
    match color:
      case "red":
        num = 0
      case "green":
        num = 1
      case "blue":
        num = 2
      case "yellow":
        num = 3
      case "purple":
        num = 4
      case "cyan":
        num = 5
      case "white":
        num = 6
      case _:
        print(f"{color} isn't a color")
        return
    self.raspbot.Ctrl_WQ2812_ALL(1, num)

  def LED_off(self):
    """Turn off LEDs"""
    self.raspbot.Ctrl_WQ2812_ALL(0, 0)
  
  # ------------- execution -------------
  
  def stop_execution(self, sig, frame):
    """Set Robot._run = False. Stops any execution loop contingent on bot.is_running()"""
    self._run = False
    print() # for terminal formatting

  def is_running(self):
    """Return the value of Robot._run (initialized True)"""
    return self._run

  # ------------- movement -------------

  def stop_motors(self):
    """Stop all wheel motors"""
    self.raspbot.Ctrl_Muto(0, 0)
    self.raspbot.Ctrl_Muto(1, 0)
    self.raspbot.Ctrl_Muto(2, 0)
    self.raspbot.Ctrl_Muto(3, 0)

  def drive_forward_forever(self, speed):
    """Drive forward with no stop"""
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)

  def drive_forward_timed(self, speed, duration):
    """Drive forward for a duration of time"""
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    time.sleep(duration)
    self.stop_motors()
    time.sleep(.1)
  
  def attack(self, speed, duration):
    """Kill"""
    self.LED_on("red")
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    time.sleep(duration)
    self.stop_motors()
    self.LED_off()
    time.sleep(.1)

  def turn_right_time(self, speed, duration):
    """Turn right for a duration of time"""
    self.raspbot.Ctrl_Muto(0, speed)
    self.raspbot.Ctrl_Muto(1, speed)
    self.raspbot.Ctrl_Muto(2, -speed)
    self.raspbot.Ctrl_Muto(3, -speed)
    time.sleep(duration)
    self.stop_motors()

  def turn_left_time(self, speed, duration):
    """Turn left for a duration of time"""
    self.raspbot.Ctrl_Muto(0, -speed)
    self.raspbot.Ctrl_Muto(1, -speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
    time.sleep(duration)
    self.stop_motors()

  def turn_right_degrees(self, speed, angle):
    """Turn right a number of degrees using the calibration table"""
    self.turn_right_time(speed, turn_time(speed, angle))
 
  def turn_left_degrees(self, speed, angle):
    """Turn left a number of degrees using the calibration table"""
    self.turn_left_time(speed, turn_time(speed, angle))
  
  def turn_left_forever(self, speed):
    self.raspbot.Ctrl_Muto(0, -speed)
    self.raspbot.Ctrl_Muto(1, -speed)
    self.raspbot.Ctrl_Muto(2, speed)
    self.raspbot.Ctrl_Muto(3, speed)
  
  def scan_left(self, speed, distance):
    """Turn left until the robot sees an object within the distance"""
    self.turn_left_forever(speed)
    while True:
      # get distance every .1 second while turning
      time.sleep(.1)
      if self.get_distance() <= distance:
        self.stop_motors()
        time.sleep(.1)
        return

  # ------------- ultrasonic -------------

  def sonic_up(self):
    """Activate ultrasonic sensor"""
    self.raspbot.Ctrl_Ulatist_Switch(1)
    time.sleep(1) # give time to calibrate

  def sonic_down(self):
    """Deactivate ultrasonic sensor"""
    self.raspbot.Ctrl_Ulatist_Switch(0)

  def get_distance(self):
    """Return distance in mm with ultrasonic sensor"""
    diss_H = self.raspbot.read_data_array(0x1b,1)[0]
    diss_L = self.raspbot.read_data_array(0x1a,1)[0]
    dis = diss_H<< 8 | diss_L
    return dis

  # ------------- light sensor -------------

  def read_data_array(self):
    """Return front light sensor data"""
    return self.raspbot.read_data_array(0x0a, 1)
