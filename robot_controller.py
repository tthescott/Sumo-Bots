import sys
import time
import bisect

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

    def turn_right_degrees(self, speed, angle):
        self.turn_right(speed, turn_time(speed, angle))

    # turn left a specific number of degrees using the calibration table
    def turn_left_degrees(self, speed, angle):
        self.turn_left(speed, turn_time(speed, angle))

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
