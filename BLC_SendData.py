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
    def publishData_main(self, patient_id, session_id, timestamp, to_bathroom, visit_length, from_bathroom, msg):
        event = HEUCOD.HeucodEvent()
        event.patient_id = patient_id
        event.value1 = session_id
        event.timestamp = timestamp
        event.value2 = to_bathroom
        event.length = visit_length        
        event.value3 = from_bathroom
        
        #Stuff not used in our database
        event.description = msg
        event.event_type = HEUCOD.HeucodEventType.BedOccupancyEvent

        publish.single(hostname="192.168.1.40",
                        port = 1883,
                        topic=f"server/main_table", 
                        payload = event.to_json())


    def publishData_dump(self, patient_id, session_id, device_id, msg):
        event = HEUCOD.HeucodEvent()

        event.patient_id = patient_id
        event.value1 = session_id
        event.timestamp = datetime.now().strftime("%D %T")        
        event.sensor_id = device_id
        event.description = msg

        #Stuff not used in our database
        event.event_type = HEUCOD.HeucodEventType.RoomMovementEvent
        print(event.to_json())
        
        
        publish.single(hostname="192.168.1.40",
                        port = 1883,
                        topic=f"server/dump_table", 
                        payload = event.to_json())
    