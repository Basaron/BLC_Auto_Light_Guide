from BLC_Model import BLCModel
from BLC_StateMachine import StateMachine
from BLC_Zigbee2mqttClient import (BLCZigbee2mqttClient,
                                   BLCZigbee2mqttMessage, BLCZigbee2mqttMessageType)
from datetime import datetime

"""This class registers events that are publsihed to the broker and handles them such that only occupancy messages from the PIR sensor and then forwarded to the StateMachine""" 
class BLCController:

    """For the connection of the broker"""
    MQTT_BROKER_HOST = "localhost"
    MQTT_BROKER_PORT = 1883 
    
    
    """ The controller is responsible for managing events received from zigbee2mqtt and handle them.
    By handle them it can be process, store and communicate with other parts of the system. In this
    case, the class listens for zigbee2mqtt events, processes them (turn on another Zigbee device)"""
    
    def __init__(self, devices_model: BLCModel) -> None:
        """ Class initializer. The actuator and monitor devices are loaded (filtered) only when the
        class is instantiated. If the database changes, this is not reflected.

        Args:
            devices_model (BLCModel): the model that represents the data of this application
        """
        
        self.__devices_model = devices_model
        self.__z2m_client = BLCZigbee2mqttClient(host=self.MQTT_BROKER_HOST,
                                                  port=self.MQTT_BROKER_PORT,
                                                  on_message_clbk=self.__zigbee2mqtt_event_received)

        self.stateMachine = StateMachine(self.__devices_model, self.__z2m_client) #Here an instance of the StateMachine is created such that it knows all the clients and devices

    
    def start(self) -> None:
        """ Start listening for zigbee2mqtt events and turn of all PIR devices"""
        self.__z2m_client.connect()
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        device = self.__devices_model.find("PIR2")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")

        

    def stop(self) -> None:
        """ Stop listening for zigbee2mqtt events.
        """
        self.__z2m_client.disconnect()


    def __zigbee2mqtt_event_received(self, message: BLCZigbee2mqttMessage) -> None:
        """ Process an event received from zigbee2mqtt. This function given as callback to
        BLCZigbee2mqttClient, which is then called when a message from zigbee2mqtt is received.

        Args:
            message (BLCZigbee2mqttMessage): an object with the message received from zigbee2mqtt
        """
        
        """Here the timestamp of the of the device is received to make sure that system operates in the valid time interval. This is done using the datetime library"""
        currecntTime = datetime.now()
        today10pm = currecntTime.replace(hour=22, minute=0, second=0, microsecond=0)    #Starting time
        today9am = currecntTime.replace(hour=9, minute=0, second=0, microsecond=0)      #Ending time

        #Making sure the time is valid
        if currecntTime > today10pm or currecntTime < today9am:
            # If message is None (it wasn't parsed), then don't do anything.
            if not message:
                return
                
            # If the message is not a device event, then don't do anything.
            if message.type_ != BLCZigbee2mqttMessageType.DEVICE_EVENT:
                return

            # Parse the topic to retreive the device ID. If the topic only has one level, don't do
            # anything.
            tokens = message.topic.split("/")
            if len(tokens) <= 1:
                return

            # Retrieve the device ID from the topic.
            device_id = tokens[1]

            # If the device ID is known, then process the device event and send a message to the remote
            # web server.
            device = self.__devices_model.find(device_id)


            #When the device that has registered movement is found by the controller, then the controller checks for a occupancy message. If there are an occupancy message, then the trigger function in the statemachine is called. Otherwise an error is returned 
            #Thus, only occupancy messages are accepted and forwarded to the state machine 
            if device:
                try:
                    occupancy = message.event["occupancy"]
                except KeyError:
                    pass
                else:
                    self.stateMachine.trigger(occupancy, device_id) #Sends the occupancy message and the device ID 

            #Occupancy message = True: PIR sensor has registered movement
            #Occuoancy message = False: PIR sensor has not registered movement 
