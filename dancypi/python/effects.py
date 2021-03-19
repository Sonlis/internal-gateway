import time
import config
import led

def CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
  for i in range(config.N_PIXELS-2):
   # led.pixels = (0,0,0)
    led.pixels = (i, red/10, green/10, blue/10)
    for j in range(EyeSize):
      led.pixels = (i+j, red, green, blue)
    led.pixels = (i+EyeSize+1, red/10, green/10, blue/10);
    led.update()
    time.sleep(SpeedDelay / 1000)
  

  time.sleep(ReturnDelay / 1000)

  for i in range(config.N_PIXELS-2, 0, -1):
    led.pixels = (0,0,0)
    led.pixels = (i, red/10, green/10, blue/10)
    for j in range(EyeSize):
      led.pixels = (i+j, red, green, blue)
    led.pixels = (i+EyeSize+1, red/10, green/10, blue/10);
    led.update()
    time.sleep(SpeedDelay / 1000)
  
 
  time.sleep(ReturnDelay / 1000)


if __name__ == '__main__':
    CylonBounce(0xff, 0x00, 0x00, 4, 10, 50);
