from enum import Enum, auto
from transitions import Machine
import time



class StateMachine:
    states = ['Bedroom', 'Room1', 'Bathroom']
    


    def __init__(self, devices_model, z2m_client):
        
        

        self.machine = Machine(
            model=self,
            states=self.states,
            initial='Bedroom',
        )
    
        self.__devices_model = devices_model
        self.__z2m_client = z2m_client
        
        self.Been_to_bath = False

        #transitions
        self.machine.add_transition('bed_to_room1', 'Bedroom','Room1', after='fun_bed_to_room1')
        self.machine.add_transition('room1_to_bed', 'Room1', 'Bedroom', after='fun_room1_to_bed')


        self.machine.add_transition('room1_to_bath', 'Room1','Bathroom', after='fun_room1_to_bath')
        self.machine.add_transition('bath_to_room1', 'Bathroom', 'Room1', after='fun_bath_to_room1')


    def trigger(self, occupancy, device_id):
        
        if self.state == 'Bedroom':
            print("Bedroom")
            if device_id == "PIR" and occupancy and not self.Been_to_bath:
                self.bed_to_room1()
            elif device_id == "PIR" and not occupancy and self.Been_to_bath:
                self.fun_bed_to_sleep()

        elif self.state == 'Room1':
            print("room1")
            if device_id == "PIR" and occupancy and self.Been_to_bath:
                self.room1_to_bed()
            elif device_id =="PIR1" and occupancy and not self.Been_to_bath:
                self.room1_to_bath()

        elif self.state == 'Bathroom':
            print("Bathroom")
            input("Pres to go out of bath room")
            if device_id =="PIR1" and occupancy:
                self.bath_to_room1()
            
        
        else:
            print("Fail in state machine")


    def fun_bed_to_room1(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledNext.id_, "ON")
        print("h1")

    def fun_room1_to_bed(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        print("h2")

    def fun_bed_to_sleep(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        self.Been_to_bath = False
        print("h3")

    def fun_room1_to_bath(self):
        device = self.__devices_model.find("PIR1")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "OFF")
        print("h4")

    def fun_bath_to_room1(self):
        device = self.__devices_model.find("PIR1")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "ON")
        self.Been_to_bath = True
        print("h5")
