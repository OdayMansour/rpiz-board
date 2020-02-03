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
  send_and_forget(url, message)


ip = '192.168.1.19'
port = '81'
url = 'ws://' + ip + ':' + port + '/'
send_and_forget(url, '{"activeProgramId": "Xv9GdRrNxTRSkZhba"}')

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
      select(url, counter%8)
    elif dtState == 0:
      while clkState != 1 or dtState != 1:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
      counter += 1
      print counter
      select(url, counter%8)

finally:
  GPIO.cleanup()

