import time, socket, sys, mraa, os
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal

led = mraa.Gpio(2)
led.dir(mraa.DIR_OUT)
 
MY_NAME = 'Edison03'

time.sleep(10)
# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

mqtt_client = paho.Client()
mqtt_topic = 'connectEdison03/' + socket.gethostname()
mqtt_client.will_set(mqtt_topic, 'Good Bye', 0, False)

broker = 'sansa.cs.uoregon.edu'
mqtt_client.connect(broker, '1883')
mqtt_client.subscribe('connectEdison03/#')

def on_connect(client, userdata, flags, rc):
  print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
  message = msg.payload
  print "message : " + message
  if "DISCONNECT" in message.strip() :
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
    sys.exit(0)

def on_disconnect(client, userdata, rc):
  print("Disconnected in a normal way")

def on_log(client, userdata, level, buf):
  receivedLog = "log: {}".format(buf) # only semi-useful IMHO
  #print(receivedLog)

# set up handlers
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log

mqtt_client.loop_start()
while True:
  response = os.system("ping -c 1 www.google.com");
  if(response == 0):
    led.write(0)
  else:
    led.write(1)
    print("****Try to quit****");
  mqtt_message = "%s " %(ip_addr) + '==== '+ MY_NAME 
  mqtt_client.publish(mqtt_topic, mqtt_message)
  time.sleep(3)
