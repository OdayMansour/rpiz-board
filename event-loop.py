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
        if state[k] != previous_state[k] and k not in ["current_program", "lights_on"]: # Do not apply when meta state changes
            previous_state[k] = state[k]
            if k == "button" and state[k] == False: # Save button off but do not apply changes
                return False
            return True
    return False


def apply_state():
    if state["button"]:
        apply_selection(url)
    else:
        change_selection(url, state["selection"])
    True



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
    print("Sending " + message)
    ws.send(message)
    ws.close()


def change_selection(url, selection):
    show_selector(url)
    message = '{"setVars": {"selected": ' + str(selection) + '}}'
    send_and_forget(url, message)
    on_lights(url)


def apply_selection(url):
    global state
    state["current_program"] = "pulse"
    send_and_forget(url, '{"activeProgramId": "rZQv9EJm736mJ9G5R"}')
    sleep(2)
    off_lights(url)


def off_lights(url):
    global state
    if state["lights_on"]:
        state["lights_on"] = False
        send_and_forget(url, '{"brightness": 0}')


def on_lights(url):
    global state
    if not state["lights_on"]:
        state["lights_on"] = True
        send_and_forget(url, '{"brightness": 0.05}')


def show_selector(url):
    global state
    if state["current_program"] != "selector":
        state["current_program"] = "selector"
        send_and_forget(url, '{"activeProgramId": "Xv9GdRrNxTRSkZhba"}')


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
        elif dtState == 0:
            while clState != 1 or dtState != 1:
                clState = GPIO.input(cl)
                dtState = GPIO.input(dt)
            counter = (counter + 1)%selections
            state["selection"] = counter


##########################
# Variables
##########################

exit_flag = False

state = {
    "selection": 0,
    "button": False,
    "rain": False,
    "proximity": False,
    "calevent": "none",
    "lights_on": True,
    "current_program": "selector"
}
previous_state = dict(state)

ip = '192.168.1.19'
port = '81'
url = 'ws://' + ip + ':' + port + '/'

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

show_selector(url)
change_selection(url, 0)
on_lights(url)

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
            print_state(False)
            apply_state()
        count += 1
        # if count > 100:
            # exit_flag = True
            # exit()

finally:
    GPIO.cleanup()

