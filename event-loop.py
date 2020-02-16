from threading import Thread
from time import sleep
from random import randrange

selection = 0

def worker(name, sleeptime):
    global selection
    
    print("Thread " + name + " started")
    while True:
        sleep(sleeptime)
        selection = randrange(30)
        print("Selection changed to " + str(selection) )


if __name__ == "__main__":
    x = Thread(target=worker, args=('worker1',2,))
    x.start()

    while True:
        sleep(0.1)
        print(selection)
