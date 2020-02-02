from websocket import create_connection
from time import sleep
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


ip = '192.168.1.19'
port = '81'
url = 'ws://' + ip + ':' + port + '/'

print 'Listing programs...'
result = send_and_receive(url, '{"listPrograms": true}')

print 'Got programs, parsing...'
trimmed_result = result[2:-1] # Removing first two binary bytes and last newline
programs = []

for program in trimmed_result.split('\n'):
  id = program.split('\t')[0]
  name = program.split('\t')[1]
  programs.append({"id": id, "name": name})

print 'Found programs: '
print programs

print 'Selecting a program at random...'
selected = programs[random.randrange(len(programs))]
print 'Selected ' + selected["id"] + ' - ' + selected["name"]

send_and_forget(url, '{"activeProgramId": "' + selected["id"] + '"}')

sleep(2)

print 'Playing around with the selected variable'

send_and_forget(url, '{"activeProgramId": "Xv9GdRrNxTRSkZhba"}')

while True:
  selected = random.randrange(8)
  print 'selected = ' + str(selected)
  message = '{"setVars": {"selected": ' + str(selected) + '}}'
  print message
  send_and_forget(url, message)
  sleep(0.5)

