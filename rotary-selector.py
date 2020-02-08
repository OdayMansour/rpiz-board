from RPi import GPIO
from time import sleep
from websocket import create_connection
import random

def send_and_receive(url, message):
  ws = create_connection(url)
  ws.send(message)
  return ws.recv()
  ws.close()


def send_and_forget(url, message):
  ws = create_connection(url)
  ws.send(message)
  ws.close()


def select(url, selection):
  message = '{"setVars": {"selected": ' + str(selection) + '}}'
  # send_and_forget(url, message)


ip = '192.168.1.19'
port = '81'
url = 'ws://' + ip + ':' + port + '/'
#send_and_forget(url, '{"activeProgramId": "Xv9GdRrNxTRSkZhba"}')

cl = 21
dt = 16
sw = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(cl, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

clState_last = GPIO.input(cl)
dtState_last = GPIO.input(dt)

try:

  while True:
    clState = GPIO.input(cl)
    dtState = GPIO.input(dt)
    swState = GPIO.input(sw)

    if clState == 0:
      while clState != 1 or dtState != 1:
        clState = GPIO.input(cl)
        dtState = GPIO.input(dt)
      counter -= 1
      print counter
      select(url, counter%8)
    elif dtState == 0:
      while clState != 1 or dtState != 1:
        clState = GPIO.input(cl)
        dtState = GPIO.input(dt)
      counter += 1
      print counter
      select(url, counter%8)
    elif swState == 0:
      print 'Switch'
      while swState == 0:
        sleep(0.05)
        swState = GPIO.input(sw)

finally:
  GPIO.cleanup()

