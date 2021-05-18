from BLC_Model import BLCModel
from BLC_StateMachine import StateMachine
from BLC_Zigbee2mqttClient import (BLCZigbee2mqttClient,
                                   BLCZigbee2mqttMessage, BLCZigbee2mqttMessageType)
from datetime import datetime

class BLCController:
    HTTP_HOST = "http://localhost:8000"
    MQTT_BROKER_HOST = "localhost"
    MQTT_BROKER_PORT = 1883

    """ The controller is responsible for managing events received from zigbee2mqtt and handle them.
    By handle them it can be process, store and communicate with other parts of the system. In this
    case, the class listens for zigbee2mqtt events, processes them (turn on another Zigbee device)
    and send an event to a remote HTTP server.
    """
    
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

        self.stateMachine = StateMachine(self.__devices_model, self.__z2m_client) 

    def start(self) -> None:
        """ Start listening for zigbee2mqtt events.
        """
        self.__z2m_client.connect()
        #print(f"Zigbee2Mqtt is {self.__z2m_client.check_health()}")
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        device = self.__devices_model.find("PIR2")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")

        self.currecntTime = datetime.datetime.now()
        self.today10pm = self.currecntTime.replace(hour=22, minute=0, second=0, microsecond=0)
        self.today9am = self.currecntTime.replace(hour=9, minute=0, second=0, microsecond=0)

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
        self.currecntTime = datetime.datetime.now()

        if self.currecntTime > self.today10pm and self.currecntTime < self.today9am:
            # If message is None (it wasn't parsed), then don't do anything.
            if not message:
                return

            #print(f"zigbee2mqtt event received on topic {message.topic}: {message.data}")

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

            if device:
                try:
                    occupancy = message.event["occupancy"]
                except KeyError:
                    pass
                else:
                    self.stateMachine.trigger(occupancy, device_id)
