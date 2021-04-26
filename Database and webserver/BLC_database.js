//Load the server using express

//To create table: CREATE TABLE `blc`.`presentation` (`id` INT KEY AUTO_INCREMENT, `topic` VARCHAR(255), `msg` VARCHAR(255), FOREIGN KEY `UsrID` REFERENCES users(id), `_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, );


const express = require('express')
var app = express()
var mysql = require('mysql'); //https://www.npmjs.com/package/mysql
var mqtt = require('mqtt');
var client = mqtt.connect('mqtt:localhost:1883')

var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC",
	database: "BLC"
});

app.listen(3000, () => {
    console.log("Test!")
})

client.on('close', (err) => {
	console.log("Looking for broker")
})

client.on('connect', (err) => {
	console.log("Connected, trying to subscribe")
	client.subscribe(Topic, mqtt_subscribe);
})

function mqtt_subscribe(err, granted) {
    console.log("Subscribed to " + Topic);
    if (err) {console.log(err);}
};

var Topic = 'server/#'; //subscribe to all topics


client.on('message', mqtt_messsageReceived);

function mqtt_messsageReceived(topic, message, packet) {
	var message_str = message.toString(); //convert byte array to string
	console.log(message_str)
	insert_message(topic, message_str)
	//message_str = message_str.replace(/\n$/, ''); //remove new line

	//payload syntax: clientID,topic,message
	/*if (countInstances(message_str) != 1) {
		console.log("Invalid payload");
		} else {	
		//insert_message(topic, message_str, packet);
		console.log(message_arr);
	}*/
};


//insert a row into the tbl_messages table
function insert_message(topic, message_str) { //topic, message_str, packet
	
	var sql = "INSERT INTO presentation (topic, msg) VALUES (?, ?)"

	connection.query(sql, [topic, message_str], (err) =>{
		if (err){
		  console.log(err);
		}
		else console.log("Inserted successfully.");
	});

	/*var message_arr = extract_string(message_str); //split a string into an array
	var clientID= message_arr[0];
	var message = message_arr[1];
	var sql = "INSERT INTO ?? (??,??,??) VALUES (?,?,?)";
	var params = ['tbl_messages', 'clientID', 'topic', 'message', clientID, topic, message];
	sql = mysql.format(sql, params);	
	
	connection.query(sql, function (error, results) {
		if (error) throw error;
		console.log("Message added: " + message_str);
	}); */
};


/*
client.on('connect', mqtt_connect);
client.on('reconnect', mqtt_reconnect);
client.on('error', mqtt_error);
client.on('close', mqtt_close);

function mqtt_connect() {
    console.log("Connecting MQTT");
    client.subscribe(Topic, mqtt_subscribe);
};




function mqtt_reconnect(err) {
    //console.log("Reconnect MQTT");
    //if (err) {console.log(err);}
	client  = mqtt.connect(Broker_URL, options);
};

function mqtt_error(err) {
    //console.log("Error!");
	//if (err) {console.log(err);}
};

function after_publish() {
	//do nothing
};
*/

//receive a message from MQTT broker






/*
function mqtt_close() {
	//console.log("Close MQTT");
};

////////////////////////////////////////////////////
///////////////////// MYSQL ////////////////////////
////////////////////////////////////////////////////



connection.connect(function(err) {
	if (err) throw err;
	console.log("Database Connected!");
});

	

//split a string into an array of substrings
function extract_string(message_str) {
	var message_arr = message_str.split(","); //convert to array	
	return message_arr;
};	

*/
//count number of delimiters in a string
var delimiter = ",";
function countInstances(message_str) {
	var substrings = message_str.split(delimiter);
	return substrings.length - 1;
};


