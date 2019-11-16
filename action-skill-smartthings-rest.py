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

def checkKey(dict, key):  
    if key in dict: 
        return True
    else:
        return False

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

def getApi(api,header,id,cmd):
    try:
        uri=api + '/device/' + str(id) + '/command/' + cmd
        response = requests.get(uri, headers=header)
    except:
        pass
def apiResponse(api,header,id):
    try:
        uri=api + '/device/' + str(id) + '/attribute/level'
        response = requests.get(uri, headers=header)
    except:
        return "None"
    finally:
        return response.json().get("value")

class Mylights(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        self.start_blocking()

    def execCommand_callback(self, hermes, intent_message):

        device=None
        myaction=None
        if intent_message.slots.device:
            device = intent_message.slots.device.first().value
        if intent_message.slots.cmd:
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
        target="none"
        if device == "lights":
            target = "all_lights"
        elif device == "lamps":
            target = "lamps"
        elif not intent_message.slots.device:
            target = "none"
        else:
            target = "one_light"
        print("target=" + str(target))
        if not intent_message.slots.device:
            if myaction == "let":
                p="and then there was light"
            else:
                p=str(saucy()) + "I have set the mood to " + myaction + " Your Magesty"
        else:
            p=str(saucy()) + "I have Turned " + myaction + " the " + device + " Your Magesty"
        for k, v in DeviceIDs.items():
            if not intent_message.slots.device:
                if myaction == "daytime":
                    if str(k) == "Basement Left":
                        getApi(api,header,str(v),"setLevel?arg=100")
                        getApi(api,header,str(v),"setHue?arg=24")
                        getApi(api,header,str(v),"setSaturation?arg=42")
                        getApi(api,header,str(v),"setColorTemperature?arg=3012")
                    elif str(k) == "Basement Right":
                        getApi(api,header,str(v),"setLevel?arg=100")
                        getApi(api,header,str(v),"setHue?arg=24")
                        getApi(api,header,str(v),"setSaturation?arg=42")
                        getApi(api,header,str(v),"setColorTemperature?arg=3012")
                    elif str(k) == "Main Area":
                        getApi(api,header,str(v),"setLevel?arg=65")
                    elif str(k) == "Bar Area":
                        getApi(api,header,str(v),"setLevel?arg=55")
                    elif str(k) == "Bar":
                        getApi(api,header,str(v),"setLevel?arg=45")
                elif myaction == "evening":
                    if str(k) == "Basement Left":
                        getApi(api,header,str(v),"setLevel?arg=80")
                        getApi(api,header,str(v),"setHue?arg=23")
                        getApi(api,header,str(v),"setSaturation?arg=52")
                        getApi(api,header,str(v),"setColorTemperature?arg=2809")
                    elif str(k) == "Basement Right":
                        getApi(api,header,str(v),"setLevel?arg=80")
                        getApi(api,header,str(v),"setHue?arg=23")
                        getApi(api,header,str(v),"setSaturation?arg=52")
                        getApi(api,header,str(v),"setColorTemperature?arg=2809")
                    elif str(k) == "Main Area":
                        getApi(api,header,str(v),"setLevel?arg=18")
                    elif str(k) == "Bar Area":
                        getApi(api,header,str(v),"off")
                    elif str(k) == "Bar":
                        getApi(api,header,str(v),"setLevel?arg=35")
                elif myaction == "let":
                    if str(k) == "Basement Left":
                        getApi(api,header,str(v),"setLevel?arg=100")
                        getApi(api,header,str(v),"setHue?arg=24")
                        getApi(api,header,str(v),"setSaturation?arg=42")
                        getApi(api,header,str(v),"setColorTemperature?arg=3012")
                    elif str(k) == "Basement Right":
                        getApi(api,header,str(v),"setLevel?arg=100")
                        getApi(api,header,str(v),"setHue?arg=24")
                        getApi(api,header,str(v),"setSaturation?arg=42")
                        getApi(api,header,str(v),"setColorTemperature?arg=3012")
                    elif str(k) == "Main Area":
                        getApi(api,header,str(v),"setLevel?arg=100")
                    elif str(k) == "Bar Area":
                        getApi(api,header,str(v),"setLevel?arg=100")
                    elif str(k) == "Bar":
                        getApi(api,header,str(v),"setLevel?arg=100")
                else:
                    hermes.publish_end_session(intent_message.session_id, "bugger, somethings a muck")
            elif str(target) == "all_lights":
                if myaction == "on" or myaction == "off":
                    getApi(api,header,str(v),myaction)
                    if myaction == "on":
                        getApi(api,header,str(v),"setLevel?arg=65")
                elif myaction == "up":
                    r=apiResponse(api,header,str(v))
                    if isinstance(r, int):
                        getApi(api,header,str(v),"setLevel?arg="+str(roundup(r)))
                elif myaction == "down":
                    r=apiResponse(api,header,str(v))
                    if isinstance(r, int):
                        getApi(api,header,str(v),"setLevel?arg="+str(rounddown(r)))
            elif str(target) == "one_light" and checkKey(DeviceIDs, device):
                print("current " + str(k))
                if str(k) == device:
                    if myaction == "on" or myaction == "off":
                        getApi(api,header,str(v),myaction)
                        hermes.publish_end_session(intent_message.session_id, p)
                    elif myaction == "up":
                        r=apiResponse(api,header,str(v))
                        print(r)
                        if isinstance(r, int):
                            getApi(api,header,str(v),"setLevel?arg="+str(roundup(r)))
                            hermes.publish_end_session(intent_message.session_id, p)
                    elif myaction == "down":
                        print(r)
                        if isinstance(r, int):
                            getApi(api,header,str(v),"setLevel?arg="+str(rounddown(r)))
                            hermes.publish_end_session(intent_message.session_id, p)
                    else:
                        hermes.publish_end_session(intent_message.session_id, "bugger, somethings a muck") 
                else:
                    hermes.publish_end_session(intent_message.session_id, "bugger, somethings a muck")    
        if str(target) == "all_lights":
            hermes.publish_end_session(intent_message.session_id, p)
        if not intent_message.slots.device:
            hermes.publish_end_session(intent_message.session_id, p)
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'hooray4me:lights':
            self.execCommand_callback(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Mylights()
