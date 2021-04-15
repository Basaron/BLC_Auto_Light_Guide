from time import sleep
from Cep2Controller import Cep2Controller
from Cep2Model import Cep2Model, Cep2ZigbeeDevicePir, Cep2ZigbeeDeviceLed


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    # divece friendly names opt/zig/data/configuration.yaml
    devices_model = Cep2Model()
    devices_model.add([Cep2ZigbeeDevicePir("0x00158d00044c228a", "pir", Cep2ZigbeeDeviceLed("0xbc33acfffe8b8d78", "led")),
                       ])

    # Create a controller and give it the data model that was instantiated.
    controller = Cep2Controller(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
