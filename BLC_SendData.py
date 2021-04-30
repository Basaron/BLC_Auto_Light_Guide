from __future__ import annotations
import json
import signal
import HEUCOD
from dataclasses import dataclass
from datetime import datetime
from distutils.util import strtobool
from queue import Empty, Queue
from threading import Event, Thread
from typing import Any, Dict, List, Union
from paho.mqtt.client import Client as MqttClient, MQTTMessage
from paho.mqtt import publish



class publisher:
    #def __init__(self):
    #    return

    def publishData(self, msg: str, val: bool, patient_id: str, start_time, visit_length):
        event = HEUCOD.HeucodEvent()
        event.description = msg
        event.timestamp = start_time #datetime.now().strftime("%D:%T")
        event.length = visit_length
        event.to_bathroom = 12
        event.from_bathroom = 14

        event.patient_id = patient_id
        event.sensor_id = 1
        
        


        print(event.to_json())

        publish.single(hostname="192.168.1.2",
                        port = 1883,
                        topic=f"server/test", 
                        payload = event.to_json())
   
if __name__ == "__main__":
    pub = publisher()

    pub.publishData("User went to bathroom", True, 1, datetime.now().strftime("%D %T"), 73)
    
