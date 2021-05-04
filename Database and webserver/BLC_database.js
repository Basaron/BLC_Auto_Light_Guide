//TODO: Throw errors to make the code not crash when uploading

//TODO: consider making the functionality to register a profile?

//TODO: tighten up the code

//TODO: Make a readme on how to setup MySQL

//TODO: make comments

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

connection.connect(function(err) {
	if (err) throw err;
	console.log("Database Connected!");
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
		console.log(topic)
		if(topic === "server/main_table"){
			insert_data_main_table(obj)
		}
		else if (topic === "server/dump_table"){
			insert_data_dump_table(obj)
		}
	}
};

//insert a row into the tbl_messages table
function insert_main(user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom) { //topic, message_str, packet
	console.log("Checkpoint 3")
	//Make the query.
	var query = "INSERT INTO main_data (user_id, session_id, start_time, time_to_bathroom, time_on_bathroom, time_from_bathroom) VALUES (?, ?, ?, ?, ?, ?)"

	connection.query(query, [user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom], (err) =>{
		if (err){
		  console.log(err);
		}
		else console.log("Inserted successfully.");
	});
};


function insert_dump(user_id, session_id, start_time, user_device_id, event) { //topic, message_str, packet

	//Make the query.
	query = "SELECT device_id FROM devices WHERE user_id = ? AND user_device_id = ?;"
	connection.query(query, [user_id, user_device_id], (err, rows) => {
		if(err){
			console.log(err)
		}
		else{
			device_id = rows[0].device_id
			console.log("THE VALUE IS: ", device_id)
			var query2 = "INSERT INTO dump_data (user_id, session_id, start_time, device_id, event) VALUES (?, ?, ?, ?, ?)"
			connection.query(query2, [user_id, session_id, start_time, device_id, event], (err) =>{
				if (err){
				console.log(err);
				}
				else console.log("Inserted successfully.");
			});
	}})
	
};


function insert_data_main_table (obj){
	var user_id = obj.patientId
	var session_id = obj.value1
	var start_time = obj.timestamp	
	var time_to_bathroom = obj.value2
	var visit_length = obj.length
	var time_from_bathroom = obj.value3

	//For viewing/developing
	console.log("User ID = ", user_id)
	console.log("Session ID = ", session_id)
	console.log("Start time = ", start_time)
	console.log("To bathroom: ", time_to_bathroom)
	console.log("Time on bathroom in seconds = ", visit_length)
	console.log("From bathroom: ", time_from_bathroom)
	
	insert_main(user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom)
	//Insert the data
	
}

function insert_data_dump_table(obj){
	var user_id = obj.patientId
	var session_id = obj.value1
	var start_time = obj.timestamp
	var user_device_id = obj.sensorId
	var event = obj.description
	
	console.log("User device ID = ", user_device_id)
	console.log("User ID = ", user_id)
	console.log("Session ID = ", session_id)
	console.log("Start time = ", start_time)
	console.log("Event = ", event)

	insert_dump(user_id, session_id, start_time, user_device_id, event)
}

//Done TODO:
//// TODO: Make the JSON object into different variables to upload

//TODO: Upload properly

//TODO: Finish the tables so that they follow the 2'nd normal

//TODO: Make a distinction between lower and upper case letters in password