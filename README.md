# RGBW_MQTT_home_assistant
Raspberry Pi connection from Digital RGBW to Home Assistant


## installation

```
nano script
```
copy past the following commands in the script

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -y
sudo pip3 install adafruit-circuitpython-neopixel 
sudo pip3 install jsonschema 
sudo pip3 install paho-mqtt 
sudo apt install git -y
git clone https://github.com/sybren-marechal/Digital_Led_Strip_MQTT.git
rm -f script
```

```
chmod +x script
time yes | sudo ./script
```

## setup
fill in the setup settings in `settings.py`

```
MQTT_BROKER = ""   # Ip adress of the MQTT Broker
MQTT_USERNAME = ""        # Username
MQTT_PASSWD = ""       # Password
MQTT_TOPIC = ""   # MQTT Topic

## setup RGB

NUMBER_OF_LEDS= 100   #int

```

## home Assistant

```
light:
  - platform: mqtt
    schema: json
    name: desk
    command_topic: "home/desk/set"
    brightness: true
    brightness_scale: 100
    rgb: true
    effect: true
    effect_list: [rainbow, set0, set1, set2, set3]
    optimistic: false
    qos: 0
```

## System D

```
chmod +x app.py

sudo su
cp service.service /etc/systemd/system
systemctl enable service.service
systemctl start service.service
```
 
to stop the service use `systemctl stop service.service`
