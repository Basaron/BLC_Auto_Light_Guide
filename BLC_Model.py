from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class Cep2ZigbeeDeviceLed:
    id_: str
    type_: str

@dataclass
class Cep2ZigbeeDevicePir:

    id_: str
    type_: str
    led_: Cep2ZigbeeDeviceLed


class Cep2Model:

    """ The model class is responsible for representing and managing access to data. In this case,
    the class is a basic dictionary that uses the devices's ID as key to reference the device
    object. This is a very simplistic database and more evolved approaches can be used. For example,
    this class might abstract the access to a database such as MySQL.
    """

    def __init__(self):
        self.__devices = {}

    """ For findig the device to resive data"""
    @property
    def actuators_list(self) -> List[Cep2ZigbeeDevicePir]:
        return list(filter(lambda s: s.type_ in {"led"},
                           self.__devices.values()))

    @property
    def devices_list(self) -> List[Cep2ZigbeeDevicePir]:
        return list(self.__devices.values())

    @property
    def sensors_list(self) -> List[Cep2ZigbeeDevicePir]:
        return list(filter(lambda s: s.type_ in {"pir"},
                           self.__devices.values()))

    def add(self, device: Union[Cep2ZigbeeDevicePir, List[Cep2ZigbeeDevicePir]]) -> None:
        """ Add a new devices to the database.

        Args:
            device (Union[Cep2ZigbeeDevicePir, List[Cep2ZigbeeDevicePir]]): a device object, or a list of
            device objects to store.
        """
        # If the value given as argument is a Cep2ZigbeeDevicePir, then create a list with it so that
        # later only a list of objects has to be inserted.
        list_devices = [device] if isinstance(device, Cep2ZigbeeDevicePir)\
            else device

        # Insert list of devices, where the device ID is the key of the dictionary.
        for s in list_devices:
            self.__devices[s.id_] = s

    def find(self, device_id: str) -> Optional[Cep2ZigbeeDevicePir]:
        """ Retrieve a device from the database by its ID.

        Args:
            device_id (str): ID of the device to retrieve.

        Returns:
            Optional[Cep2ZigbeeDevicePir]: a device. If the device is not stored, then None is returned
        """
        # Use the bult-in function filter to get the device. The output of filter is a filter object
        # that is then casted to a list. The, the first result, if any, is returned; otherwise None.
        # Instead of None, am exception can also be raised.
        devices = list(filter(lambda kv: kv[0] == device_id,
                              self.__devices.items()))

        return devices[0][1] if len(devices) >= 1 else None