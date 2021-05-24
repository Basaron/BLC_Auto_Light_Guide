from enum import Enum, auto
from transitions import Machine
from BLC_SendData import publisher
from datetime import datetime
import time

"""This class implements the transitions when the user moves from one room to another. Thus, each room acts as a state in the system"""

class StateMachine:
    states = ['Bedroom', 'Room1', 'Room2', 'Bathroom'] #Creates the states according to the rooms in the building 

    def __init__(self, devices_model, z2m_client):
    
        """ constructor: 
        The bedroom is set as the starting state."""
        self.machine = Machine(
            model=self,
            states=self.states,
            initial='Bedroom',
        )
    
        #Instances of the devices and the zigbee client is also instantiated
        self.__devices_model = devices_model
        self.__z2m_client = z2m_client
        

        #True/false variable decribing if the user has been to the bathroom. Used to determine the direction of logic in the StateMachine
        self.Been_to_bath = False 
        
        #Time measurements of the user movements 
        self.awake =0
        self.start_to_bath =0
        self.finish_to_bath =0
        self.start_in_bath =0
        self.finish_in_bath  =0
        self.start_from_bath =0
        self.finish_from_bath =0
        
        #Instantiates the publisher and a counter for number of times the user has been to the bathroom 
        self.pub = publisher()
        self.sesion = 1
        
        #transitions for the StateMachine. Implemented using the transitions library 
        self.machine.add_transition('bed_to_room1', 'Bedroom','Room1', after='fun_bed_to_room1')
        
        self.machine.add_transition('room1_to_room2', 'Room1','Room2', after='fun_room1_to_room2')
        self.machine.add_transition('room1_to_bed', 'Room1', 'Bedroom', after='fun_room1_to_bed')

        self.machine.add_transition('room2_to_bath', 'Room2', 'Bathroom', after='fun_room2_to_bath')
        self.machine.add_transition('room2_to_room1', 'Room2', 'Room1', after='fun_room2_to_room1')

        self.machine.add_transition('bath_to_room2', 'Bathroom', 'Room2', after='fun_bath_to_room2')


    #StateMachine logic:
    #Gets called from the controller, which states which PIR sensors that have registered movement 
    def trigger(self, occupancy, device_id):
        
        #State 1 : Bedroom 
        if self.state == 'Bedroom':
            print("Bedroom")
            if device_id == "PIR" and occupancy and not self.Been_to_bath:  #Describes the transition from the bedroom to room1. 
                self.bed_to_room1()                                         #If the deviceID = LED and occupancy = true and the user has not been to the bathroom yet, then bed-to-room1 transition is called (This means the user has waken up and needs to go to the toilet) 
            elif device_id == "PIR" and not occupancy and self.Been_to_bath:
                self.fun_bed_to_sleep()                                     #If the deviceID = LED and occupancy = true and the has been to the bathroom, then bed-to-sleep transition is called (This means the user is back from the bathroom)

        #State 2 : Room 1
        elif self.state == 'Room1':
            print("room1")
            if device_id == "PIR" and occupancy and self.Been_to_bath:
                self.room1_to_bed()
            elif device_id =="PIR1" and occupancy and not self.Been_to_bath:
                self.room1_to_room2()

        #State 3 : Room 2
        elif self.state == 'Room2':
            print("room2")
            if device_id == "PIR1" and occupancy and self.Been_to_bath:
                self.room2_to_room1()
            elif device_id =="PIR2" and occupancy and not self.Been_to_bath:
                self.room2_to_bath()

        #State 4 : Bathroom 
        elif self.state == 'Bathroom':
            print("Bathroom")
            
            if device_id =="PIR3" and occupancy and not self.Been_to_bath:
                self.fun_in_bath()
            elif device_id =="PIR2" and occupancy and self.Been_to_bath:
                self.bath_to_room2()
            
        #If error occurs an error message is written (Logging is preffered here)  
        else:
            print("Fail in state machine")

            
    #Functions to describe the transitions itself 
    def fun_bed_to_room1(self):
        device = self.__devices_model.find("PIR")                                           #Getting the correct deviceID
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")                             #Changing the state of the LED in the room, so it is now on 
        self.__z2m_client.change_state(device.ledNext.id_, "ON")                            #Changing the state of the LED in the next room, so it is now off
        self.awake = datetime.now().strftime("%D %T") #Format: date - current time          #Gets the current time 
        self.start_to_bath = time.time()                                                    #Keeps track of the time during the transition 
        self.pub.publishData_dump(1,    self.sesion,       1,      "Movement detected")     #Publishing data to the database (occupancy message)

    def fun_room1_to_room2(self):
        device = self.__devices_model.find("PIR1")                                          #Getting the correct deviceID
        self.__z2m_client.change_state(device.ledNext.id_, "ON")                            
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "OFF")                            #Turning off the LED in the former room 
        self.pub.publishData_dump(1,    self.sesion,       2,      "Movement detected")     #publishData(patientID, sessionID, deviceID, message)
    
    def fun_room2_to_bath(self):
        device = self.__devices_model.find("PIR2")
        self.__z2m_client.change_state(device.ledNext.id_, "ON")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "OFF")
        self.pub.publishData_dump(1,    self.sesion,       3,      "Movement detected")
    
    #This function determines when the user has been to the bathroom. Here the logic changes for the state machine and now "reverses"
    def fun_in_bath(self):
        self.finish_to_bath = time.time()             
        self.start_in_bath = time.time()
        self.Been_to_bath = True                                                            #User has been to bathroom.
        self.pub.publishData_dump(1,    self.sesion,       4,      "Movement detected")


    def fun_bath_to_room2(self):
        device = self.__devices_model.find("PIR2")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")                           #User returns from the bathroom, so the "next" LED is now the previous LED and has to turned off
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "ON")
        self.finish_in_bath = time.time()
        self.start_from_bath = time.time()
        self.pub.publishData_dump(1,    self.sesion,       3,      "Movement detected")

    def fun_room2_to_room1(self):
        device = self.__devices_model.find("PIR1")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledPre.id_, "ON")
        self.pub.publishData_dump(1,    self.sesion,       2,      "Movement detected")

    def fun_room1_to_bed(self):
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "ON")
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        self.pub.publishData_dump(1,    self.sesion,       1,      "Movement detected")
        self.finish_from_bath = time.time()

    def fun_bed_to_sleep(self):                                     
        device = self.__devices_model.find("PIR")
        self.__z2m_client.change_state(device.ledOwn.id_, "OFF")               #Turning off the rest of the LEDs
        self.__z2m_client.change_state(device.ledNext.id_, "OFF")
        
        #Calculating the amount of times the user spends going to the bathroom, being on the bathroom and going back to the bedroom. 
        to_bathroom = int(self.finish_to_bath - self.start_to_bath)            
        on_bathroom = int(self.finish_in_bath - self.start_in_bath)
        from_bathroom = int(self.finish_from_bath - self.start_from_bath)
        
        print("to bathroom = ", to_bathroom, ", on bathroom = ", on_bathroom, " and from bathroom = ", from_bathroom)
        self.pub.publishData_main(1, self.sesion, self.awake, to_bathroom, on_bathroom, from_bathroom, "User went to bathroom and back to bed") #Publishing the time data to the webserver
        self.sesion += 1
        
        self.Been_to_bath = False #Resetting the variable back to false
        
