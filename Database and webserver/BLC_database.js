//TODO: Throw errors to make the code not crash when uploading

//TODO: make comments

//Load the server using express
var mysql = require('mysql'); 
var mqtt = require('mqtt'); //For connecting to the broker
var client = mqtt.connect('mqtt:localhost:1883') //Connect to the local broker on standard port

//Creating the mySQL connection for the database on port 3306 on localhost, with the user root. 
var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC", //!The root password, if this is not the root password, change it. Otherwise it can't connect
	database: "BLC"
});

//For connecting to the mySQL database
connection.connect(function(err) {
	if (err) throw err;
	console.log("Database Connected!"); //print to console
});

//If no broker is found
client.on('close', (err) => {
	if (err) {console.log(err)}
	console.log("Looking for broker") //print to console
})

var Topic = 'server/#'; //subscribe to all topics under the 'server/' topic
//If connected to the broker
client.on('connect', (err) => {
	if (err) {console.log("huh", err)} //Prints a JSON packet, i dont know what it means, but i assume return code 0 is fine, and it works as intended
	console.log("Connected, trying to subscribe") //print to console
	client.subscribe(Topic, mqtt_subscribe); //Subscribe to the topic 'server/#'
})

function mqtt_subscribe(err, granted) {
    //Simply prints info
	if (err) {console.log(err);}
	console.log("Subscribed to " + Topic); 
    
};


//If a message is recieved, go to the function that handles it
client.on('message', mqtt_messsageReceived);

//For handling a recieved message
function mqtt_messsageReceived(topic, message) {
	//Get the send data into JSON
	const obj = JSON.parse(message)
	//If it recieves something empty, its an invalid payload.
	if (Object.keys(obj).length === 0) { 
		console.log("Invalid payload");	
	}

	//If not, split the data into variables. Check if its for the dump or for the main table
	else {
		//If its for the main table
		console.log(topic)
		if(topic === "server/main_table"){
			split_data_main(obj)
		}
		//If its for the dump table
		else if (topic === "server/dump_table"){
			split_data_dump(obj)
		}
		//If its neither of the topics above.
		else{
			console.log("Recieved on wrong topic.")
		}
	}
};


//Insert a row into the tbl_messages table
function insert_main(user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom) { //topic, message_str, packet
	//Make the query.
	var query = "INSERT INTO main_data (user_id, session_id, start_time, time_to_bathroom, time_on_bathroom, time_from_bathroom) VALUES (?, ?, ?, ?, ?, ?)"

	connection.query(query, [user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom], (err) =>{
		//Execute the query with the input values
		if (err){
		  console.log(err); //If error, log it
		}
		else console.log("Inserted successfully."); //If no error, do nothing
	});
};


function insert_dump(user_id, session_id, start_time, user_device_id, event) { //topic, message_str, packet

	//Make the query. The query gets the actual device_id by using the user and the Pi's believed device_id
	query = "SELECT device_id FROM devices WHERE user_id = ? AND user_device_id = ?;"
	connection.query(query, [user_id, user_device_id], (err, rows) => {
		if(err){
			console.log(err)
		} 
		else{
			//Nested query calls seems stupid, but the scopes in Javascript are weird, and its the only way i could use the
			//value device_id, as i otherwise can't save it to outside of the scope. Returning the value doesnt work either.
			device_id = rows[0].device_id //Get the device ID
			console.log("THE VALUE IS: ", device_id)
			var query2 = "INSERT INTO dump_data (session_id, start_time, device_id, event) VALUES (?, ?, ?, ?, ?)"
			connection.query(query2, [session_id, start_time, device_id, event], (err) =>{ //Execute the query with the input values
				if (err){
				console.log(err); //If error, log it
				}
				else console.log("Inserted successfully."); //If no error, do nothing
			});
	}})	
};


function split_data_main (obj){
	//Split up the JSON object
	var user_id = obj.patientId
	var session_id = obj.value1
	var start_time = obj.timestamp	
	var time_to_bathroom = obj.value2
	var visit_length = obj.length
	var time_from_bathroom = obj.value3
	
	//For viewing/developing
	// console.log("User ID = ", user_id)
	// console.log("Session ID = ", session_id)
	// console.log("Start time = ", start_time)
	// console.log("To bathroom: ", time_to_bathroom)
	// console.log("Time on bathroom in seconds = ", visit_length)
	// console.log("From bathroom: ", time_from_bathroom)

	//Insert the data
	insert_main(user_id, session_id, start_time, time_to_bathroom, visit_length, time_from_bathroom)
	
}


function split_data_dump (obj){
	//Split up the JSON object
	var user_id = obj.patientId
	var session_id = obj.value1
	var start_time = obj.timestamp
	var user_device_id = obj.sensorId
	var event = obj.description

	//For viewing/developing	
	// console.log("User_id =", user_id)
	// console.log("User device ID = ", user_device_id)
	// console.log("Session ID = ", session_id)
	// console.log("Start time = ", start_time)
	// console.log("Event = ", event)
	
	//Insert the data
	insert_dump(user_id, session_id, start_time, user_device_id, event)
}

//Done TODO:

//TODO: Split the JSON object into different variables to upload

//TODO: Upload properly to mySQL

//TODO: Finish the tables so that they follow the 2'nd normal standard

//TODO: Make a distinction between lower and upper case letters in password

//TODO: remove user_id from dump table, as it can be accessed through the device_id

//TODO: consider making the functionality to register a profile?

//TODO: tighten up the code

//TODO: Make a readme on how to setup MySQL