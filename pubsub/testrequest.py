import time, socket, sys, os
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal

def control_c_handler(signum, frame):
  mqtt_client.disconnect()
  mqtt_client.loop_stop()
  sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

mqtt_client = paho.Client()
mqtt_topic = 'joback/' + socket.gethostname()
mqtt_client.will_set(mqtt_topic, 'Good Bye', 2, False)
broker = 'sansa.cs.uoregon.edu'
mqtt_client.connect(broker, '1883')
mqtt_client.subscribe('joback/#')

def on_connect(client, userdata, flags, rc):
  print('connected')

def on_message(client, userdata, msg):
  message = msg.payload
  print "message : " + message

def on_disconnect(client, userdata, rc):
  print("Disconnected in a normal way")

def on_log(client, userdata, level, buf):
  receivedLog = "log: {}".format(buf)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log
mqtt_client.loop_start()

def main(): 
  while True:
    mqtt_client.publish(mqtt_topic, "PROCESS", 2, False)
    time.sleep(3)

main()
