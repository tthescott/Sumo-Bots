import time
import board
import adafruit_tcs34725

i2c = board.I2C()

sesnor = adafruit_tcs34725.TCS34725(i2c)
sesnor.gain = 16
sesnor.integration_time = 50

try:
  while True:
    temp = sesnor.color_temperature
    lux = sesnor.lux
    rgb = sesnor.color_rgb_bytes

    # print(sesnor.color_raw)
    print(f"Temp: {temp}K, Lux: {lux}, RGB: {rgb}")
  
    if (rgb[0] > 2 * rgb[1] and rgb[0] > 2 * rgb[2]):
      print("red")
    elif (rgb[1] > 2 * rgb[0] and rgb[1] > 2 * rgb[2]):
      print("green")
    elif (rgb[2] > 2 * rgb[0] and rgb[2] > 2 * rgb[1]):
      print("blue")

    time.sleep(1)

except KeyboardInterrupt:
  print()
