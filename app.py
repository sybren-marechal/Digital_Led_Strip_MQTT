#!/usr/bin/env python3
import time
import board
import neopixel
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from lib.led import *
from jsonschema import validate
from settings import *

led = None
loopflag = False

full_state_schema = {
    "type" : "object",
    "properties" : {
        "state" : {"enum" : ["ON", "OFF"]},
        "effect" : {"enum" :["rainbow", "set0", "set1", "set2", "set3"]},
        "brightness" : {"type": "number", "minimum": 0, "maximum": 255 },
        "color": {
            "type" : "object",
            "properties" : {
                "r" : {"type": "number", "minimum": 0, "maximum": 255 },
                "g" : {"type": "number", "minimum": 0, "maximum": 255 },
                "b" : {"type": "number", "minimum": 0, "maximum": 255 }
            },
            "required": ["r", "g", "b"]
        }
    }
}

def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
  
def on_message(client, userdata, msg):
    global json_message, loopflag, animation
    json_message = str(msg.payload.decode("utf-8"))
    print("message received: ", json_message)

    try:
        data = json.loads(json_message)
        # validate(data, full_state_schema)
        if len(data) == 1:
            if "state" in data.keys():
                if data['state'] == "ON":
                    print("state" , data['state']) # then you can check the value
                    led.all_on()
                if data['state'] == "OFF":
                    print("state" , data['state']) # then you can check the value
                    led.all_off()
        else:
            if "brightness" in data.keys():
                led.set_brightness(data['brightness'])

            if "color" in data.keys():
                led.set_color(data['color']['g'], data['color']['r'], data['color']['b'])
     
            if "effect" in data.keys():
                loopflag = True
                if (data['effect'] == 'rainbow'):
                    animation = 'rainbow'
                elif (data['effect'] == 'set0'):
                    animation = 'set0'
                elif (data['effect'] == 'set1'):
                    animation = 'set1'
                elif (data['effect'] == 'set2'):
                    animation = 'set2'
                elif (data['effect'] == 'set3'):
                    animation = 'set3'
            else:
                animation = 'none'
                loopflag = False

                # publish_state(client)
    except exceptions.ValidationError:
        print ("Message failed validation")
 
    except ValueError:
        print ("Invalid json string")

if __name__ == '__main__':       
    led = Led(board.D18, NUMBER_OF_LEDS , 0.1)
     
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER,1883,60)
    client.username_pw_set(username=MQTT_USERNAME,password=MQTT_PASSWD)
    publish.single("Boot", "Hello World", hostname=MQTT_BROKER ,auth={'username':MQTT_USERNAME,'password':MQTT_PASSWD})
    client.loop_start()

    justoutofloop = False
    print ('Press Ctrl-C to quit.')
    while True:
        if loopflag and animation != 'none':
            justoutofloop = True
            if animation == 'rainbow':
                led.rainbow_cycle() 
            elif (animation == 'set0'):
                led.set0()
            # elif (animation == 'set1'):
            #     led.set1()
            # elif (animation == 'set2'):
            #     led.set2(Color(randint(0,255), randint(0,255), randint(0,255)))
            # elif (animation == 'set3'):
            #     led.set3(Color(randint(0,127), randint(0,127), randint(0,127)))
        if not loopflag and justoutofloop:
            justoutofloop = False
        time.sleep(.1)
    client.disconnect()
    client.loop_stop()
