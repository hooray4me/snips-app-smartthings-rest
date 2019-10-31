#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests
import json

CONFIG_INI = "config.ini"

MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

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
        print(token)
        print(api)
        auth = 'Bearer ' + token
        header = {'Authorization': auth, 'Content-Type': 'application/json'}
        d=self.config.get("secret").get("devices")
#        DeviceIDs = ['09b0803c-cfe3-4b8a-8fc0-e8161701ade4', '2537cac5-2c28-454f-bdc2-5741ae4c44c4',  '7c792f42-a018-4664-af72-d41cf93b49df', '1d9b3329-4d6f-493d-baac-1ee84cec75e8', '5d5a7635-f1a5-40ac-ad1f-d75967545824']
        a= [ d ]
        print(a)
        DeviceIDs = dict(s.split(':') for s in a)
        print(DeviceIDs)
        print(len(DeviceIDs))
        #print(DeviceIDs['Main Area'])
        if device == "lights":
            target = "all_lights"
        elif device == "lamps":
            target = "lamps"
        else:
            target == "one_light"
        if target == "all_lights":
            if myaction == "on" or myaction == "off":
                for index in range(len(DeviceIDs)):
                    #uri=api + '/device/' + DeviceIDs[index] + '/command/' + myaction
                    print(DeviceIDs[index])
                    #print(uri)
                    #print(header)
                    #response = requests.get(uri, headers=header)
                hermes.publish_end_session(intent_message.session_id, "Turning " + myaction + " " + device)
        else:
            hermes.publish_end_session(intent_message.session_id, "Be boop be be boop, somethings not right")

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
