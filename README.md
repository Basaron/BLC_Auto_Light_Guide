**Welcome to BLC's Automated Ligth Guide!** 

In here you find the source code of the automated light guide, developed by Blinding Lights Cooporations. 


# Setting up the database and webserver

First, install node.js - [Download link](https://nodejs.org/en/), take the left version reccomended for most users.

Make sure you have version 6.X:

	$ npm -v

Download the zip files, unzip and navigate to the *Database and webserver* folder in a console.

From the folder, the needed libraries should already by set and ready to go, located in the *node_modules* folder. If, for some unknown reason, this is now the case, you can install all the libraries with the following command line:

	$ npm install -g nodemon body-parser express-ejs-layouts express-session js-sha256 ejs mysql mqtt

With the libraries installed, we now move on to install the database. For this, we use mySQL.
We uses mySQL Workbench for a better viewing experience, and will give a walkthrough on it. If you wish to set it up in a console instead, you can do so, too. 

To get the mySQL Workbench, install the bottom version on [this link.](https://dev.mysql.com/downloads/installer/). 

You can skip the account setup, and just download the software right away. For the installation, follow the developer default setup. For the root password you can set it what you wish it to be. It is set to ```BLC``` in the code (both in BLC_webserver.js and BLC_databse.js), and if you set the code to something else, you must change this at both occurrence.

The mySQL Workbench should automatically opens. Under mySQL connections should be an already created connection - click it to enter it, with the password chosen.

In the workbench, choose "Create a new schema" and create one called *blc* with default settings:

![How to make schema](https://github.com/Biorrith/Software-Teknologi/blob/main/pictures/schema.png)

Now execute the following commands, one at a time:

```
CREATE TABLE blc.devices(
			device_id INT AUTO_INCREMENT NOT NULL, 
			user_id INT NOT NULL, 
			device_type VARCHAR(30) NOT NULL, 
			device_location VARCHAR (30) NOT NULL,
			user_device_id int,
			PRIMARY KEY (device_id)
			);
```


