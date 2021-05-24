from time import sleep
from BLC_Controller import BLCController
from BLC_Model import BLCModel, BLCZigbeeDevicePir, BLCZigbeeDeviceLed


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    # Device friendly names opt/zig/data/configuration.yaml
    devices_model = BLCModel()

    #The PIR is created through the model class using the add function.   
    devices_model.add([BLCZigbeeDevicePir("PIR", "pir", None ,BLCZigbeeDeviceLed("LED", "led0"), BLCZigbeeDeviceLed("LED1", "led1")),                                   #Bedroom PIR
                       BLCZigbeeDevicePir("PIR1", "pir", BLCZigbeeDeviceLed("LED", "led0"),BLCZigbeeDeviceLed("LED1", "led1"), BLCZigbeeDeviceLed("LED2", "led2")),     #Room1 PIR1
                       BLCZigbeeDevicePir("PIR2", "pir", BLCZigbeeDeviceLed("LED1", "led1"),BLCZigbeeDeviceLed("LED2", "led2"), BLCZigbeeDeviceLed("LED3", "led3")),    #Room2 PIR2
                       BLCZigbeeDevicePir("PIR3", "pir", None, None, None)                                                                                              #Bathroom PIR3
                       ])

    # Create a controller and give it the data model that was instantiated.
    controller = BLCController(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
