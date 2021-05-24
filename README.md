# Welcome to BLC's Automated Ligth Guide!

In here you find the source code of the automated light guide, developed by Blinding Lights Cooporations. Additionally, there is a walkthrough on how to set up the system, including descriptions on setting up the database, installing the MQTT broker, setting up the automated light guide and more.


# Setting up the database and webserver

First, install node.js - [Download link](https://nodejs.org/en/), take the left version reccomended for most users.

Make sure you have version 6.X:

	$ npm -v
	
	

Download the zip files, unzip and navigate to the *Database and webserver* folder in a console.

From the folder, the needed libraries should already by set and ready to go, located in the *node_modules* folder, except for express. Install express with the following command, which should be executed in the *Database and webserver* directory:
	
	$ npm install express

If, for some unknown reason, the libraries gives an error, you can install all the libraries with the following command line in the *node_modules* directory:

	$ npm install body-parser express-ejs-layouts express-session js-sha256 ejs mysql mqtt

With the libraries installed, we now move on to install the database. For this, we use mySQL.

**MySQL**

We uses mySQL Workbench for a better viewing experience, and will give a walkthrough on it. If you wish to set it up in a console instead, you can do so, too. 

To get the mySQL Workbench, install the bottom version on [this link.](https://dev.mysql.com/downloads/installer/). 

You can skip the account setup, and just download the software right away. For the installation, follow the developer default setup. For the root password you can set it what you wish it to be. It is set to ```BLC``` in the code (both in BLC_webserver.js and BLC_databse.js), and if you set the code to something else, you must change this at both occurrence.

The mySQL Workbench should automatically opens. Under mySQL connections should be an already created connection - click it to enter it, with the password chosen.

In the workbench, choose "Create a new schema" and create one called *blc* with default settings:

![How to make schema](https://github.com/Biorrith/Software-Teknologi/blob/main/pictures/schema.png)

Next, create a new SQL tab: ![How to make new SQL tab](https://github.com/Basaron/BLC_Auto_Light_Guide/blob/main/Pictures/query.png):
In the tab, insert and execute the following query, by clicking the 'lightning' button:

```
CREATE TABLE blc.devices(
			device_id INT AUTO_INCREMENT NOT NULL, 
			user_id INT NOT NULL, 
			device_type VARCHAR(30) NOT NULL, 
			device_location VARCHAR (30) NOT NULL,
			user_device_id int NOT NULL,
			PRIMARY KEY (device_id)
			);

CREATE TABLE blc.users  (
			user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,  
		 	username VARCHAR(64) NOT NULL,  
			psw VARCHAR(64) NOT NULL, 
			PRIMARY KEY (user_id)
			);

CREATE TABLE blc.main_data 	
			(
			event_id INT KEY AUTO_INCREMENT NOT NULL, 
			user_id INT UNSIGNED NOT NULL, 
			session_id int NOT NULL,
			start_time VARCHAR(30) NOT NULL,  
			time_to_bathroom VARCHAR(30) NOT NULL, 
			time_on_bathroom VARCHAR(30) NOT NULL,  
			time_from_bathroom VARCHAR(30) NOT NULL, 
			FOREIGN KEY (user_id) REFERENCES users(user_id)
			);

CREATE TABLE blc.dump_data
			(
			event_id INT KEY AUTO_INCREMENT NOT NULL, 
			session_id INT NOT NULL,
			start_time VARCHAR(30) NOT NULL,
			device_id int NOT NULL, 
			event VARCHAR (255) NOT NULL, 
			FOREIGN KEY (device_id) REFERENCES devices(device_id)
			);

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'BLC'
```
The last command, ALTER USER, sets the root password of the user. If you chose another password earlier, you have to alter this in the command, too. Now that all tables are created, everything should be set and ready to go. However, inserting users and devices into the system must be done manually. And example of inserting such follows:
```
INSERT INTO blc.users (username, psw) VALUES ("BLC", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3");
```
Here, you insert the username BLC and the password 123. However, since the login is running with SHA256 hash, when inserting the password, you must insert the encrypted version of the password. You can use [this site](https://emn178.github.io/online-tools/sha256.html) to do so.
An example of inserting devices:

```
INSERT INTO blc.devices (user_id, device_type, device_location, user_device_id) VALUES (1, "PIR", "Bedroom", 1);
```

Here, user_id, device type and location are self explanatory. The user device ID is the device ID used on the respective users pi. For this, bedroom should always be 1, and the bathrooom always be the last.

**MQTT broker**

In order to get the data from the Pi, a MQTT broker is required to be running on the host machine. There are numerous tutorials online on how to download and install such. For Windows, go to [this site](https://mosquitto.org/download/) to download the broker. For Linux, run the following command

	$ install mosquitto mosquitto-clients

Which should automatically install the broker and run it as a daemon.

**Running the code**

Now everything should be set up and ready to run. To run the code, you can install nodemon in the *Database and webserver* directory:

	$ npm install -g nodemon
	
Open the *Database and webserver* in two consoles, and run the two files, one to retrieve data and one to make the website, with the following commands:

	$ nodemon BLC_webserver.js
	
	$ nodemon BLC_database.js

If, for some unfortunate reason, nodemon is not recognized, you can also run the programs with:

	$ node BLC_webserver.js
	
	$ node BLC_database.js


Now your server should be up and running on a localhost, port 3000. To acces it on a webbrowser from the same machine as the server is hosted on, simply type in internet address:

	localhost:3000

To connect to the server from other devices on the same LAN, connect via the IPv4 adress, port 3000. To connect to the browser, type the following as the internet address:

	'IPv4 address':3000
	
With the specific IPv4 address instead of 'IPv4 address'.


# Setting up the Automated Light Guide
For Setting up the Automated Light Guide, you will need: four GL-MC-001 LEDS, four Aqara motion Sensor, one Zigbee USB adapter and a Rasberry PI 4 Kit. On the Rasberry PI, there has to be the following installed: Python3, Node JS, MQTT broker, Zigbee2Mqtt and a python library called transitions.

**MQTT**

Please refer to the tutorial from the database guide.

**Zigbee2MQTT**

To install Zigbee2MQTT, please refer to [this link.](https://github.com/Basaron/BLC_Auto_Light_Guide/blob/main/References/CEP2%20TUTORIAL%203.pdf). Once installed, connect the devices. 

For running the code, we give the devices more userfriendly names. This can be done in the /opt/zigbee2mqtt/data/configuration.yaml file, located on the PI. Change the devices names to the names shown in [the following picture (please excuse the quality).](https://github.com/Basaron/BLC_Auto_Light_Guide/blob/main/Pictures/configuration.yaml.png)

Importantly, this has to bee done after all the wanted devices are connected to zigbee, as the devices will otherwise not appear.

**Transitions library**

To install the library, simply open a treminal and run the following code:

	$ pip3 install transitions

**Running the code for the Automated Light Guide**

For this, Zigbee2Mqtt has to be started by executing the following commands in a new terminal:

	$cd /opt/zigbee2mqtt
	
	$npm start

Secondly, you must first clone the repository, and in a console navigate to the *RasPi_Code* folder. In the new console, to run the code, simply execute the following command:

	$python3 BLC_Main.py


**Adding/removing more Sensor and LED**
The automated light guide is scalable with minor changes in the source code.
First, add/remove the friendly name to the configuration.yaml file, in order to access it in the code.

Then, the device has to bee added manually in BLC_main.py like the following:

```python
#The PIR is created through the model class using the add function.   
    devices_model.add([BLCZigbeeDevicePir("PIR", "pir", None ,BLCZigbeeDeviceLed("LED", "led0"), BLCZigbeeDeviceLed("LED1", "led1")),                                   #Bedroom PIR
                       BLCZigbeeDevicePir("PIR1", "pir", BLCZigbeeDeviceLed("LED", "led0"),BLCZigbeeDeviceLed("LED1", "led1"), BLCZigbeeDeviceLed("LED2", "led2")),     #Room1 PIR1
                       BLCZigbeeDevicePir("PIR2", "pir", BLCZigbeeDeviceLed("LED1", "led1"),BLCZigbeeDeviceLed("LED2", "led2"), BLCZigbeeDeviceLed("LED3", "led3")),    #Room2 PIR2
                       BLCZigbeeDevicePir("PIR3", "pir", None, None, None)                                                                                              #Bathroom PIR3
                       ])
```

Then in the BLC_StateMachine.py There will need to be add a new state and then the correspondig new transitions. From the new states to the preexisting states


```python
#State 3 : Room 2
        elif self.state == 'Room2':
            print("room2")
            if device_id == "PIR1" and occupancy and self.Been_to_bath:
                self.room2_to_room1()
            elif device_id =="PIR2" and occupancy and not self.Been_to_bath:
                self.room2_to_bath()
```

```python
 self.machine.add_transition('room2_to_bath', 'Room2', 'Bathroom', after='fun_room2_to_bath')
        self.machine.add_transition('room2_to_room1', 'Room2', 'Room1', after='fun_room2_to_room1')

        self.machine.add_transition('bath_to_room2', 'Bathroom', 'Room2', after='fun_bath_to_room2')
```





