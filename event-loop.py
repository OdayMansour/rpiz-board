from threading import Thread
from time import sleep
from os import system

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



##########################
# Background functions
##########################

def selector_tracker():
    global state
    global exit_flag

    while not exit_flag:
        state["selection"] = random.randrange(30)
        sleep(random.uniform(0,4))


def proximity_tracker():
    global state
    global exit_flag

    while not exit_flag:
        if (state["proximity"]):
            sleep(0.5)
            state["proximity"] = False
        else:
            sleep(random.uniform(0,2))
            if (random.random() > 0.7):
                state["proximity"] = True


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



##########################
# Set up environment
##########################

random.seed()



##########################
# Background threads
##########################

thread_selector = Thread(target=selector_tracker)
thread_proximity = Thread(target=proximity_tracker)
# thread_rain = Thread(target=rain_tracker)
# thread_calevent = Thread(target=calevent_tracker)

thread_selector.start()
thread_proximity.start()
# thread_rain.start()
# thread_calevent.start()



##########################
# Main loop
##########################

count = 0

while True:
    sleep(0.1)
    if state_change():
        print_state(True)
    count += 1
    if count > 150:
        exit_flag = True
        exit()


