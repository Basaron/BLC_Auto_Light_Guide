from time import sleep
from BLC_Controller import Cep2Controller
from BLC_Model import Cep2Model, Cep2ZigbeeDevicePir, Cep2ZigbeeDeviceLed


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    # divece friendly names opt/zig/data/configuration.yaml
    devices_model = Cep2Model()
    devices_model.add([Cep2ZigbeeDevicePir("PIR", "pir", Cep2ZigbeeDeviceLed("LED", "led")),
                       ])

    # Create a controller and give it the data model that was instantiated.
    controller = Cep2Controller(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
