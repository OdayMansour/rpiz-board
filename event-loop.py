from RPi import GPIO
from threading import Thread
from time import sleep
from os import system
from websocket import create_connection

import random
import sys


##########################
# State functions
##########################

def print_state(clear):
    if clear:
        system("clear")
    for k in state:
        print(k + " = " + str(state[k]))
    print()


def state_change():
    for k in state:
        if state[k] != previous_state[k]:
            previous_state[k] = state[k]
            return True
    return False


def apply_state():
    select(url, state["selection"])



##########################
# Interface functions
##########################

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


##########################
# Background functions
##########################

def button_tracker():
    global state
    global exit_flag
    global sw

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while not exit_flag:
        swState = GPIO.input(sw)

        if swState == 0:
            state["button"] = True
            while swState == 0:
                sleep(0.05)
                swState = GPIO.input(sw)
            state["button"] = False


def rotator_tracker():

    global state
    global exit_flag
    global cl
    global dt

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cl, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    counter = 0
    selections = 8

    clState_last = GPIO.input(cl)
    dtState_last = GPIO.input(dt)

    while not exit_flag:
        clState = GPIO.input(cl)
        dtState = GPIO.input(dt)

        if clState == 0:
            while clState != 1 or dtState != 1:
                clState = GPIO.input(cl)
                dtState = GPIO.input(dt)
            counter = (counter - 1)%selections
            state["selection"] = counter
            # select(url, counter%8)
        elif dtState == 0:
            while clState != 1 or dtState != 1:
                clState = GPIO.input(cl)
                dtState = GPIO.input(dt)
            counter = (counter + 1)%selections
            state["selection"] = counter
            # select(url, counter%8)


##########################
# Variables
##########################

exit_flag = False

state = {
    "selection": 0,
    "button": False,
    "rain": False,
    "proximity": False,
    "calevent": "none"
}
previous_state = dict(state)

ip = '192.168.1.19'
port = '81'
url = 'ws://' + ip + ':' + port + '/'
send_and_forget(url, '{"activeProgramId": "Xv9GdRrNxTRSkZhba"}')

cl = 21
dt = 16
sw = 20


##########################
# Set up environment
##########################

random.seed()

GPIO.setmode(GPIO.BCM)
GPIO.setup(cl, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    

##########################
# Background threads
##########################

thread_button = Thread(target=button_tracker)
thread_rotator = Thread(target=rotator_tracker)
# thread_rain = Thread(target=rain_tracker)
# thread_calevent = Thread(target=calevent_tracker)

thread_button.start()
thread_rotator.start()
# thread_rain.start()
# thread_calevent.start()


##########################
# Main loop
##########################

count = 0

try:

    while True:
        # sleep(0.01)
        if state_change():
            print_state(True)
            apply_state()
        count += 1
        # if count > 100:
            # exit_flag = True
            # exit()

finally:
    GPIO.cleanup()

