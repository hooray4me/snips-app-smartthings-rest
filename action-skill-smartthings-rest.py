#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests
import json
import math
import random
CONFIG_INI = "config.ini"

MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def saucy():
    i=["and if by some means of sourcery ","try not to be like a democrat ","dont get your knickers in a twist ","sheesh ","good gravy ","i give and i give and i give ","if I did not know any better you would think i am your slave ","barking orders i see do not forget i know where the bodies are burried ","it is time for a drink "]
    return random.choice(i)

def roundup(x):
    i=[20,30,40,50,60,70,80,90]
    if (x in i):
        x=x+1
    y = int(math.ceil(x / 10.0)) * 10
    if y > 100:
        return 100
    else:
        return y

def rounddown(x):
    i=[20,30,40,50,60,70,80,90]
    if (x in i):
        x=x-1
    y = int(math.floor(x / 10.0)) * 10
    if y < 10:
        return 10
    else:
        return y

class Mylights(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        self.start_blocking()

    def execCommand_callback(self, hermes, intent_message):

        device = intent_message.slots.device.first().value
        myaction = intent_message.slots.cmd.first().value
        token = self.config.get("secret").get("bearer-auth-token")
        api = self.config.get("secret").get("rest-api-url")
        auth = 'Bearer ' + token
        header = {'Authorization': auth, 'Content-Type': 'application/json'}
        d=self.config.get("secret").get("devices")
        a=d.split(",")
        DeviceIDs = dict(s.split(':') for s in a)
        print(DeviceIDs)
        print(device)
        if device == "lights":
            target = "all_lights"
        elif device == "lamps":
            target = "lamps"
        else:
            target = "one_light"

        print("target=" + str(target))
#        if target == "all_lights":
#            if myaction == "on" or myaction == "off":
#                for k, v in DeviceIDs.items():
#                    #uri=api + '/device/' + str(v) + '/command/' + myaction
#                    uri=api + '/device/' + str(v) + '/attribute/level'
#                    response = requests.get(uri, headers=header)
#                    r =response.json().get("value")
#                    print(k)
#                    print(r)
#                    if isinstance(r, int):
#                        print(roundup(r))
#                        print(rounddown(r))
        for k, v in DeviceIDs.items():
            if str(target) == "all_lights":
                if myaction == "on" or myaction == "off":
                    uri=api + '/device/' + str(v) + '/command/' + myaction
                    response = requests.get(uri, headers=header)

                elif myaction == "up":
                    uri=api + '/device/' + str(v) + '/attribute/level'
                    response = requests.get(uri, headers=header)
                    r=response.json().get("value")
                    if isinstance(r, int):
                        uri=api + '/device/' + str(v) + '/command/setLevel?arg=' + str(roundup(r))
                        response = requests.get(uri, headers=header)

                elif myaction == "down":
                    uri=api + '/device/' + str(v) + '/attribute/level'
                    response = requests.get(uri, headers=header)
                    r=response.json().get("value")
                    if isinstance(r, int):
                        uri=api + '/device/' + str(v) + '/command/setLevel?arg=' + str(rounddown(r))
                        response = requests.get(uri, headers=header)

            elif str(target) == "one_light":
                print("current " + str(k))
                if str(k) == device:
                    if myaction == "on" or myaction == "off":
                        uri=api + '/device/' + str(v) + '/command/' + myaction
                        response = requests.get(uri, headers=header)

                    elif myaction == "up":
                        uri=api + '/device/' + str(v) + '/attribute/level'
                        response = requests.get(uri, headers=header)
                        r=response.json().get("value")
                        print(r)

                        if isinstance(r, int):
                            uri=api + '/device/' + str(v) + '/command/setLevel?arg=' + str(roundup(r))
                            print(uri)
                            response = requests.get(uri, headers=header)

                    elif myaction == "down":
                        uri=api + '/device/' + str(v) + '/attribute/level'
                        response = requests.get(uri, headers=header)
                        r=response.json().get("value")
                        print(r)
                        if isinstance(r, int):
                            uri=api + '/device/' + str(v) + '/command/setLevel?arg=' + str(rounddown(r))
                            print(uri)
                            response = requests.get(uri, headers=header)

        if myaction == "on" or myaction == "off":
            p=str(saucy()) + "I have Turned " + myaction + " the " + device + " Your Magesty"
            print(str(p))
            hermes.publish_end_session(intent_message.session_id, p)
        elif myaction == "up" or myaction == "down":
            p=str(saucy()) + "I have Turned " + myaction + " the " + device + " Your Magesty"
            print(str(p))
            hermes.publish_end_session(intent_message.session_id, p)
        else:
            hermes.publish_end_session(intent_message.session_id, "bugger, somethings a muck")

    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'hooray4me:lights':
            self.execCommand_callback(hermes, intent_message)


    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Mylights()
