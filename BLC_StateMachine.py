from enum import Enum, auto
from transitions import Machine
from BLC_SendData import publisher
from datetime import datetime
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
        self.awake =0
        self.start_to_bath =0
        self.finish_to_bath =0
        self.start_in_Bath =0
        self.finish_in_Bath  =0
        self.start_from_bath =0
        self.finish_from_bath =0
        
        self.pub = publisher()
        self.sesion = 1
        
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
        self.awake = datetime.now().strftime("%D %T") #Format: date - current time
        self.start_to_bath = time.time()#datetime.now().replace(microsecond=0)
        self.pub.publishData_dump(1,    self.sesion,       1,      "Movement detected")
        

    def fun_room1_to_bed(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        self.pub.publishData_dump(1,    self.sesion,       1,      "Movement detected")
        self.finish_from_bath = time.time()#datetime.now().replace(microsecond=0)
        print("h2")

    def fun_bed_to_sleep(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        
        
        to_bathroom = int(self.finish_to_bath - self.start_to_bath)
        #to_bathroom.strftime("%T")
        on_bathroom = int(self.finish_in_Bath - self.start_in_Bath)
        #on_bathroom.strftime("%T")
        from_bathroom = int(self.finish_from_bath - self.start_from_bath)
        #from_bathroom.strftime("%T")
        
        print("to bathroom = ", to_bathroom, ", on bathroom = ", on_bathroom, " and from bathroom = ", from_bathroom)
        self.pub.publishData_main(1, self.sesion, self.awake, to_bathroom, on_bathroom, from_bathroom, "User went to bathroom and back to bed")
        self.sesion += 1
        
        self.Been_to_bath = False
        print("h3")

    def fun_room1_to_bath(self):
        device = self.__devices_model.find("PIR1")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "OFF")
        self.finish_to_bath = time.time()#datetime.now().replace(microsecond=0)
        self.start_in_bath = time.time()#datetime.now().replace(microsecond=0)
        self.pub.publishData_dump(1,    self.sesion,       2,      "Movement detected")
        print("h4")

    def fun_bath_to_room1(self):
        device = self.__devices_model.find("PIR1")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "ON")
        self.finish_in_bath = time.time()#datetime.now().replace(microsecond=0)
        self.start_from_bath = time.time()#datetime.now().replace(microsecond=0)
        self.pub.publishData_dump(1,    self.sesion,       3,      "Movement detected")
        self.pub.publishData_dump(1,    self.sesion,       2,      "Movement detected")
        self.Been_to_bath = True
        print("h5")
