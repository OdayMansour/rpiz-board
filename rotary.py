from RPi import GPIO
from time import sleep

clk = 21
dt = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

clkState_last = GPIO.input(clk)
dtState_last = GPIO.input(dt)

try:

  while True:
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)

    if clkState == 0:
      while clkState != 1 or dtState != 1:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
      counter -= 1
      print counter
    elif dtState == 0:
      while clkState != 1 or dtState != 1:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
      counter += 1
      print counter

finally:
  GPIO.cleanup()

