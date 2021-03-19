import time
import config
import led
import numpy as np
from random import random, randrange

r = [None] * config.N_PIXELS
g = [None] * config.N_PIXELS
b = [None] * config.N_PIXELS


def CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
  r = [None] * config.N_PIXELS
  g = [None] * config.N_PIXELS
  b = [None] * config.N_PIXELS
  for i in range(config.N_PIXELS-EyeSize-2):
    r[i] = red/10
    g[i] = green/10
    b[i] = blue/10
    for j in range(EyeSize):
      r[i+j] = red
      g[i+j] = green
      b[i+j] = blue
    r[i+EyeSize+1] = red/10
    g[i+EyeSize+1] = green/10 
    b[i+EyeSize+1] = blue/10
    led.pixels = np.array([r, g,b]) 
    led.update()
    time.sleep(SpeedDelay / 1000)
  time.sleep(ReturnDelay / 1000)

  for i in range(config.N_PIXELS-EyeSize-2, 0, -1):
    r[i] = red/10
    g[i] = green/10
    b[i] = blue/10
    for j in range(EyeSize):
      r[i+j] = red
      g[i+j] = green
      b[i+j] = blue
    r[i+EyeSize+1] = red/10
    g[i+EyeSize+1] = green/10 
    b[i+EyeSize+1] = blue/10
    led.update()
    time.sleep(SpeedDelay / 1000)
  
 
  time.sleep(ReturnDelay / 1000)

def Fire(Cooling, Sparking, SpeedDelay):
  global cooldown, heat, y, r, g, b
  heat = list(range(config.N_PIXELS))
  for i in range(config.N_PIXELS):
    cooldown = randrange(0, ((Cooling * 10) / config.N_PIXELS) +2)
    if cooldown > heat[i]:
      heat[i] = 0
    else:
      heat[i] = heat[i] - cooldown 
  for k in range(config.N_PIXELS - 1, 2, -1):
    heat[k] = (heat[k - 1] + heat[k - 2] + heat[k -2]) / 3
  if randrange(255) < Sparking:
    y = randrange(7)
    heat[y] = heat[y] + randrange(160,255)
  for j in range(config.N_PIXELS):
    r, g, b = setPixelHeatColor(j, heat[j])
  led.pixels = np.array([r,g,b])
  led.update()
  time.sleep(SpeedDelay / 1000)

def setPixelHeatColor(Pixel, temperature):
  global r, g, b
  t192 = int(round((temperature / 255.0)*191))
  heatramp = t192 & 0x3F
  heatramp <<= 2
  if (t192 > 0x80):
    r[Pixel] = 255
    g[Pixel] = 255
    b[Pixel] = heatramp 
  elif (t192 > 0x40):
    r[Pixel] = 255
    g[Pixel] = heatramp
    b[Pixel] = 0
  else:
    r[Pixel] = heatramp 
    g[Pixel] = 0
    b[Pixel] = 0 
  return r, g, b

if __name__ == '__main__':
    while True:
      CylonBounce(0xff, 0x00, 0x00, 4, 10, 50)
      #Fire(55,120,50)
