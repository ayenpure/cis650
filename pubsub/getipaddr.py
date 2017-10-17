import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal

MY_NAME = 'Abhishek'

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

# Instantiate the MQTT client
mqtt_client = paho.Client()
mqtt_topic = 'connectEdison03/' + socket.gethostname()
mqtt_client.will_set(mqtt_topic, 'Good Bye', 0, False)
broker = 'sansa.cs.uoregon.edu'
mqtt_client.connect(broker, '1883')
mqtt_client.subscribe('connectEdison03/#')

def control_c_handler(signum, frame):
  mqtt_client.disconnect()
  mqtt_client.loop_stop()
  sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)


def on_connect(client, userdata, flags, rc):
  print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
  message = msg.payload
  print("message = " + message)
  details = message.split("====");
  if "Edison03" in details[1].strip():
    ipfile = open("/home/abhishek/edisonip", "w")
    ipfile.write(details[1].strip())
    ipfile.write("\n")
    ipfile.write(details[0].strip())
    mqtt_client.publish(mqtt_topic, "DISCONNECT")
    time.sleep(10);
    mqtt_client.disconnect();
    mqtt_client.loop_stop();
    sys.exit();

def on_disconnect(client, userdata, rc):
  print("Disconnected in a normal way")

def on_log(client, userdata, level, buf):
  receivedLog = "log: {}".format(buf) # only semi-useful IMHO
  print(receivedLog)

# set up handlers
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log

mqtt_client.loop_start()
while True:
  time.sleep(3)
