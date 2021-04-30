//TODO: Throw errors to make the code not crash when uploading

//TODO: consider making the functionality to register a profile?

//TODO: tighten up the code

//TODO: Make a readme on how to setup MySQL

//TODO: make comments

//TODO: Make a distinction between lower and upper case letters in password?

//Load the server using express
var mysql = require('mysql'); 
var mqtt = require('mqtt'); //For connecting to the broker
var client = mqtt.connect('mqtt:localhost:1883') //Connect to the local broker on standard port

//Creating the mySQL connection for the database.
var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC",
	database: "BLC"
});

//If no broker is found
client.on('close', (err) => {
	console.log("Looking for broker")
})

//If connected to the broker
client.on('connect', (err) => {
	console.log("Connected, trying to subscribe")
	client.subscribe(Topic, mqtt_subscribe); //Subscribe
})

function mqtt_subscribe(err, granted) {
    console.log("Subscribed to " + Topic);
    if (err) {console.log(err);}
};


var Topic = 'server/#'; //subscribe to all topics in server

//If a message is recieved, go to the function that handles it
client.on('message', mqtt_messsageReceived);

//For handling a recieved message
function mqtt_messsageReceived(topic, message, packet) {
	
	//Get the send data into JSON
	const obj = JSON.parse(message) //.toString()


	//If it recieves something empty, its an invalid payload.
		//Maybe consider if it should be when it recieves something of different length then
		//expected.	
	if (Object.keys(obj).length === 0) { 
		console.log("Invalid payload");
		
	}
	//If not, split the data into variables.
	else {
		var description = obj.description
		var start_time = obj.timestamp	
		var visit_length = obj.length
		var user_id = obj.patientId
		var sensor_id = obj.sensorId
		var time_to_bathroom = obj.toBathroom
		var time_from_bathroom = obj.fromBathroom
	
		//For viewing/developing
		console.log(description)
		console.log("Start time = ", start_time)
		console.log("Time on bathroom in seconds = ", visit_length)
		console.log("To bathroom: ", time_to_bathroom)
		console.log("Patient ID = ", user_id)
		console.log("Sensor ID = ", sensor_id)
		
		//Insert the data
		insert_message(description, start_time, time_to_bathroom, visit_length, time_from_bathroom, sensor_id, user_id)
	}	
};

//insert a row into the tbl_messages table
function insert_message(description, start_time, time_to_bathroom, visit_length, time_from_bathroom, sensor_id, user_id) { //topic, message_str, packet
	
	//Make the query.
	var query = "INSERT INTO data (dscription, start_time, time_to_bathroom, time_on_bathroom, time_from_bathroom, device_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"

	connection.query(query, [description, start_time, time_to_bathroom, visit_length, time_from_bathroom, sensor_id, user_id], (err) =>{
		if (err){
		  console.log(err);
		}
		else console.log("Inserted successfully.");
	});
};

connection.connect(function(err) {
	if (err) throw err;
	console.log("Database Connected!");
});


//Done TODO:
//// TODO: Make the JSON object into different variables to upload

//TODO: Upload properly

//TODO: Finish the tables so that they follow the 2'nd normal