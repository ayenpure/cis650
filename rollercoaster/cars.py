from enum import Enum
import paho.mqtt.client as paho
import time

NUM_CARS = 1

class State(Enum):
  READY = 0
  RIDING = 1
  ARRIVE = 2
  SOCIALGROUP = 3

class Car:
  state = State.READY

  def advanceState(self):
    self.state = State((self.state.value + 1) % 4)
    print self.state.name

car = Car()

def on_connect(client, userdata, flags, rc):
  print "Connected"

def on_message(client, userdata, msg):
  message = msg.payload
  print message
  if "PICKUP" in message :
    car.advanceState()
        
def on_disconnect(client, userdata, rc):
  print "Disconnected"

def on_log(client, userdata, level, buf):
        receivedLog = "log: {}".format(buf) # only semi-useful IMHO
        print(receivedLog)

mqtt_client = paho.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log
mqtt_topic = 'cis650/somethingcool' # don't change this or you will screw it up for others 
 
# See https://pypi.python.org/pypi/paho-mqtt#option-functions. 
mqtt_client.will_set(mqtt_topic, '______________Will of someone cool _________________\n\n', 0, False) 
broker = 'sansa.cs.uoregon.edu'  # Boyana's server 
# Public brokers: https://github.com/mqtt/mqtt.github.io/wiki/public_brokers, e.g., 'test.mosquitto.org' 
mqtt_client.connect(broker, '1883') 
# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe. 
# If you do list more than one topic, consdier using message_callback_add for each topic as described above. 
# For below, wild-card should do it. 
mqtt_client.subscribe('cis650/somethingcool') #subscribe to all students in class 
mqtt_client.loop_start()


def getVacantCar(listofCars) :
  print "Searching a free car"

def main():
  print "I am here"
  while True:
    time.sleep(1)

main()
