
//Libraries
const express = require('express') //For setting up the website
const bodyParser = require('body-parser') //For getting the input data
const session = require('express-session'); //For making sessions for the logged in user

var crypto = require('crypto') //For password encryption
var mysql = require('mysql'); //Connecting to the database

var app = express()
app.use(bodyParser.urlencoded({extended:true})) //For displaying the HTML files
app.use('/assets', express.static('assets')); //To access the CSS style
app.use('/pictures',  express.static('pictures')); //To access the pictures for styling

app.use(session({
	secret: '123456cat',
	resave: false,
	username: '', //Used to safe the user logged in
	saveUninitialized: true,
	cookie: {
		expires: 3600000 //Expires after an hour
	}
  }));

app.set('view engine', 'ejs') //To get the ejs files as the view.

//Start the server on localhost port 3000
app.listen(3000, () => {
    console.log("Server up and running")
})

//Creating the mySQL connection for the database on port 3306, localhost, with the user root. 
var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC", //!The root password, if this is not the root password, change it. Otherwise it can't connect
	database: "BLC"
});

//SHA256 encryption for the password
function createHash(string_input){
	const hash = crypto.createHash('sha256')
	hash.update(string_input);
	return hash.digest('hex');
  }	

//When accessing the frontpage, show the 'login' ejs file for the homepage.
app.get('/', (req, res) => {
	res.render('login');
})

//Called by the login ejs file, and authendicates the inserted username and password.
app.post('/login', (req, res) => {
	var username = req.body.username //Get username
	var password = createHash(req.body.password) //Get encrypyed password
	var query = 'SELECT * FROM users WHERE username = ? AND psw = ?' //Query for checking if the user is in the database
	
	
	connection.query(query, [username, password], (err, rows) => { //Execute the query
		if (err){
			console.log(err);
		  }
		else{
			if(rows.length > 0) { //If any result (hence larger than 0)
				req.session.username = rows[0].user_id//user id
      			req.session.loggedin = true; //Say logged in true

				res.redirect('/homepage') //Go to the homepage
			}
			else{
				console.log("Wrong username or password") //If no match is found in the database
				res.render('login', {message: "Wrong username or password"}) //Re render the login page an with error message
			}
		}
	})
})

//The homepage for the logged in user.
app.get('/homepage', (req, res) => { //TODO: Make the actual homepage
	if (!req.session.loggedin){
		res.redirect('/')
	} //If not logged in, go to the login page.

	else{ //If logged in, get username for personalized homepage :)
	
		var query = "SELECT username FROM users WHERE user_id = ?;"
		console.log(req.session.username)
		connection.query(query, [req.session.username], (err, rows) =>{
			if(err) console.log(err)
			else {
				console.log(rows)
				res.render('homepage', {title: 'User data', userData: rows}) //Render the homepage with the username
			}
		})
	}
})

//If the logged out button is clicked on the homepage, end the session and go to the front page
app.get('/logout', (req, res) => { //TODO Make this a proper logout with ending session
	req.session.destroy();
	res.redirect('/');
  })

//View the data from the main table
app.get('/view', (req, res) => {
	if (!req.session.loggedin) res.redirect('/') //If not logged in, redirect to frontpage
	else{
		query = "SELECT * FROM main_data WHERE user_id = ?" //Get all data for the specific user
		connection.query(query, [req.session.username], (err, rows, fields) => { //TODO: make this to user the session user ID instead of 1
		//Execute the query
			if(err){
				console.log(err)
			}
			console.log(rows)
			res.render('data', {title: 'User data', userData: rows}) //Send the data to the ejs file to display with HTML
		})
	}
})

//View the data from the dump table
app.get('/dump', (req, res) => {
	if (!req.session.loggedin) res.redirect('/') //If not logged in, redirect to frontpage
	else{
		//Get all data for the specific user
		var query = "SELECT dump_data.start_time, dump_data.event, devices.device_location FROM dump_data INNER JOIN devices ON dump_data.device_id=devices.device_id WHERE devices.user_id = ? ORDER BY start_time;"
		
		connection.query(query, [req.session.username], (err, rows, fields) => {
			if (err) console.log(err)
			else{
				res.render('dump', { title: 'dump', userData: rows}) //Send the data to the ejs file to display with HTML
			}
		})
	} 
})

//Get details from a specific session ID the on main table
app.get('/details/:id', (req, res) =>{
	if (req.session.loggedin){
	//Get all the data where the the session ID and session username (stored in 
	//the devices table, accessed with a foreign key) fit, ordered by start time.
	var query = "SELECT dump_data.start_time, dump_data.event, devices.device_location FROM dump_data INNER JOIN devices ON dump_data.device_id=devices.device_id WHERE session_id = ? AND devices.user_id = ? ORDER BY start_time;"
	const session_id = req.params.id
	
	connection.query(query, [session_id, req.session.username], (err, rows, fields) => { //Execute query
  		if (err) console.log(err)
		else{
				console.log(rows)
				res.render('details', { title: 'data', userData: rows}) //Send the data to the ejs file to display with HTML
			}
		})
	} 
	
	else res.redirect('/') //If not logged in, redirect to frontpage
  })


//Done TODOS

//TODO: make hash of password

//TODO: Make sessions using cookies, and only make '/' accessible if not logged in. 

//TODO: Implement the login system

//TODO: hash password

//TODO: Get data down from the database with foreign keys: https://dba.stackexchange.com/questions/129023/selecting-data-from-another-table-using-a-foreign-key

//TODO: Make a proper website

//TODO: Make comments

//TODO: Tighten up the code