import time
import config
import led
import numpy as np
from random import random, randrange, randint
import sys

r = [0] * config.N_PIXELS
g = [0] * config.N_PIXELS
b = [0] * config.N_PIXELS
heat = [0] * config.N_PIXELS

def CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
  global r,g,b
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
  global heat
  for i in range(config.N_PIXELS):
    cooldown = randint(0,round(((Cooling * 10) / config.N_PIXELS) +2))
    if cooldown > heat[i]:
      heat[i] = 0
    else:
      heat[i] = heat[i] - cooldown 
  for k in range(config.N_PIXELS - 1, 2, -1):
    heat[k] = (heat[k - 1] + heat[k - 2] + heat[k -2]) / 3
  if randint(0,255) < Sparking:
    y = randint(0,7)
    heat[y] = randint(160,255)
  for j in range(config.N_PIXELS):
    print(heat[j])
    r[j], g[j], b[j] = setPixelHeatColor(heat[j])
  led.pixels = np.array([r,g,b])
  led.update()
  time.sleep(SpeedDelay / 1000)

def setPixelHeatColor(temperature):
  c = [bytes] * 3
  t192 = round((temperature / 255)*191)
  heatramp = t192 & 0x3F
  heatramp <<= 2
  if (t192 & 0x80):
    c[0] = 255
    c[1] = 255
    c[2] = heatramp 
  elif (t192 & 0x40):
    c[0] = 255
    c[1] = heatramp
    c[2] = 0
  else:
    c[0] = heatramp 
    c[1] = 0
    c[2] = 0 
  return c

def colorWipe(rcolor,gcolor,bcolor, wait_ms=50):
    global r,g,b
    """Wipe color across display a pixel at a time."""
    for i in range(config.N_PIXELS):
      r[i] = rcolor
      g[i] = gcolor
      b[i] = bcolor 
      led.pixels = np.array([r,g,b])
      led.update()
      time.sleep(wait_ms/1000.0)

def theaterChase(rcolor, gcolor, bcolor, wait_ms=50):
  global r,g,b
  """Movie theater light style chaser animation."""
  for q in range(3):
    for i in range(0, config.N_PIXELS, 3):
      r[i+q] = rcolor
      g[i+q] = gcolor
      b[i+q] = bcolor
    led.pixels = np.array([r,g,b])
    led.update()
    time.sleep(wait_ms/1000.0)
    for i in range(0, config.N_PIXELS, 3):
      r[i+q] = 0
      g[i+q] = 0
      b[i+q] = 0
    led.pixels = np.array([r,g,b])

def rainbow(wait_ms=20, iterations=1):
  for j in range(256*iterations):
    for i in range(config.N_PIXELS):
      r[i], g[i], b[i] = wheel(round(((i * 256 / config.N_PIXELS) +j)) & 255)
    led.pixels = np.array([r,g,b])
    led.update()
    time.sleep(wait_ms/1000.0)

def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
  c = [bytes] * 3
  if pos < 85:
    c[0] = pos*3
    c[1] = 144 - pos * 3
    c[2] = 0
  elif pos < 170:
    pos -= 85
    c[0] = 144 - pos * 3
    c[1] = 0
    c[2] = pos * 3
  else:
    pos -= 170
    c[0] = 0
    c[1] = pos * 3
    c[2] = 255 - pos * 3
  return c

def theaterChaseRainbow(wait_ms=50):
  for j in range(256):
    for q in range(3):
      for i in range(0, config.N_PIXELS, 3):
        r[i+q], g[i+q], b[i+q] = wheel((i+j) % 255)
      led.pixels = np.array([r,g,b])
      led.update()
      time.sleep(wait_ms/1000.0)
      for i in range(0, config.N_PIXELS, 3):
        r[i+q] = 0
        g[i+q] = 0
        b[i+q] = 0
      led.pixels = np.array([r,g,b])

  

def clear():
  global r, g, b
  for i in range(config.N_PIXELS):
    r[i] = 0
    g[i] = 0
    b[i] = 0
  led.pixels = np.array([r,g,b])
  led.update()



if __name__ == '__main__':
  if sys.argv[1] == "color_wipe":
    while True:
      colorWipe(255,0,0)
  elif sys.argv[1] == "theater_chase":
    while True:
      theaterChase(127,127,127)
  elif sys.argv[1] == "rainbow":
    while True:
      rainbow()
  elif sys.argv[1] == "theater_chase_rainbow":
    while True:
      theaterChaseRainbow()
  elif sys.argv[1] == "fire":
    while True:
      Fire(70,120,30)
  elif sys.argv[1] == "clear":
    clear()
