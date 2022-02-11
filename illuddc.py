#!/bin/python

# author: Claudio Bräuer
# mail: contact at cvbrauer dot de

# python dependencies: requests, subprocess, time, json, sys
# system dependencies: dccutil

import subprocess
import requests
import time
import json
import sys

# set your private home assistant rest token
token = "SECRETTOKEN"
# set the sensor name that you want to query
sensor = "sensor.balcony_light_illuminance_lux"
# set the relevant json field name
field = "illuminance_lux"
# set host ip and port
host = "192.168.0.1:8123"
# set illuminance value at which the monitor is set to maximum brightness
illuminance_max = 10000
# set illuminance value at which the monitor is set to minimum brightness
illuminance_min = 500
# set maximum monitor brightness
brightness_max = 100
# set minimum monitor brightness
brightness_min = 20
# set query interval in seconds
interval = 60
# get the id of the corresponding ddc brightness parameter, typically it is 10
ddcattr = "10"
# verify TLS certificate? Set to false because of reasons
verifyTLS = False


headers = {'Authorization': 'Bearer ' + token, 'Content-Type': "application/json"}
target = "https://" + host + "/api/states/" + sensor

while True:
    # lazy catchall
    try:
        response = requests.get(target, headers=headers, verify=verifyTLS).text
    except:
        continue
    # json to dict
    responseJson = json.loads(response)
    # for debugging purposes, print json to understand structure:
    print(responseJson)
    # set corresponding dictionary path to field here, e.g "attributes"-> "illuminance_lux"
    illuminance_cur = responseJson['attributes'][field]
    # clamping the values to min or max
    if illuminance_cur <= illuminance_min:
        illuminance_cur = illuminance_min
    if illuminance_cur >= illuminance_max:
        illuminance_cur = illuminance_max
    # linear interpolation
    brightness = ((illuminance_cur - illuminance_min) / (illuminance_max - illuminance_min)) * (brightness_max - brightness_min) + brightness_min
    # set display brightness via ddcutil and go to sleep
    spargs = ['ddcutil', 'setvcp', ddcattr, str(int(brightness))]
    subprocess.call(spargs)
    time.sleep(interval)
