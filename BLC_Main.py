from time import sleep
from BLC_Controller import BLCController
from BLC_Model import BLCModel, BLCZigbeeDevicePir, BLCZigbeeDeviceLed


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    # divece friendly names opt/zig/data/configuration.yaml
    devices_model = BLCModel()
    devices_model.add([BLCZigbeeDevicePir("PIR", "pir0", None ,BLCZigbeeDeviceLed("LED", "led0"), BLCZigbeeDeviceLed("LED1", "led1")),
                       BLCZigbeeDevicePir("PIR1", "pir1", BLCZigbeeDeviceLed("LED", "led0"),BLCZigbeeDeviceLed("LED1", "led1"), BLCZigbeeDeviceLed("LED2", "led2")),
                       BLCZigbeeDevicePir("PIR2", "pir2", BLCZigbeeDeviceLed("LED1", "led1"),BLCZigbeeDeviceLed("LED2", "led2"), BLCZigbeeDeviceLed("LED3", "led3")),
                       BLCZigbeeDevicePir("PIR3", "pir3", None, None, None)
                       ])

    # Create a controller and give it the data model that was instantiated.
    controller = BLCController(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
