import HEUCOD
from datetime import datetime
from paho.mqtt import publish


class publisher:
    def publishData_main(self, patient_id, session_id, timestamp, to_bathroom, visit_length, from_bathroom, msg):
        event = HEUCOD.HeucodEvent()
        event.patient_id = patient_id
        event.value1 = session_id
        event.timestamp = timestamp #Input timestamp, as it should be from the first movement in the bedroom,
        #And if we logged it here, it would be the last movement in bedroom
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
        event.timestamp = datetime.now().strftime("%D %T")#Save here, as its called the same time user is in room.
        event.sensor_id = device_id
        event.description = msg

        #Stuff not used in our database
        event.event_type = HEUCOD.HeucodEventType.RoomMovementEvent
        print(event.to_json())
        
        
        publish.single(hostname="192.168.1.40",
                        port = 1883,
                        topic=f"server/dump_table", 
                        payload = event.to_json())
    