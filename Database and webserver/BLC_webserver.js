//TODO: Make sessions using cookies, and only make '/' accessible if not logged in. 

//TODO: Implement the login system

//TODO: hash password

//TODO: Make a proper website

//TODO: Get data down from the database with foreign keys: https://dba.stackexchange.com/questions/129023/selecting-data-from-another-table-using-a-foreign-key

//TODO: Make comments

//TODO: Tighten up the code

//Libraries
const express = require('express') //For setting up the website
const bodyParser = require('body-parser') //For getting the input data
const session = require('express-session');


var userID //TODO: find a better way to store userID (perhaps with sessions?)
var crypto = require('crypto')
var mysql = require('mysql'); //Connecting to the database

const { connect } = require('mqtt');
var app = express()
app.use(bodyParser.urlencoded({extended:true}))
app.use('/assets', express.static('assets')); //To access the CSS style
app.use('/pictures',  express.static('pictures')); //To access the CSS style

app.use(session({
	secret: '123456cat',
	resave: false,
	username: '',
	saveUninitialized: true,
	cookie: {
		expires: 3600000 //An hour
	}
  }));

app.set('view engine', 'ejs')

app.listen(3000, () => {
    console.log("Server up and running")
})

var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC",
	database: "BLC"
})



function createHash(string_input){
	const hash = crypto.createHash('sha256')
	hash.update(string_input);
	return hash.digest('hex');
  }

app.get('/', (req, res) => {
	res.render('login');
})

app.get('/view', (req, res) => {
	if (!req.session.loggedin) res.redirect('/') //If not logged in
	else{
	query = "SELECT * FROM data WHERE user_id = ?"
	connection.query(query, [req.session.username], (err, rows, fields) => { //TODO: make this to user the session user ID instead of 1
		if(err){
			console.log(err)
		}
		res.render('data', {title: 'User data', userData: rows})
	})
	}
})
  
app.get('/homepage', (req, res) => { //TODO: Make the actual homepage
	if (!req.session.loggedin){
		res.redirect('/')
	} //If not logged in
	else{
	
	var query = "SELECT username FROM users WHERE user_id = ?;"
	console.log(req.session.username)
	connection.query(query, [req.session.username], (err, rows) =>{
		if(err) console.log(err)
		else {
			console.log(rows)
			res.render('homepage', {title: 'User data', userData: rows})
	}
	})
	}
})

app.get('/logout', (req, res) => { //TODO Make this a proper logout with ending session
	req.session.destroy();
	res.redirect('/');
  })

app.post('/login', (req, res) => {
	var username = req.body.username
	var password = createHash(req.body.password)
	//TODO: make hash of password
	var query = 'SELECT * FROM users WHERE username = ? AND psw = ?'
	
	connection.query(query, [username, password], (err, rows) => {
		if (err){
			console.log(err);
		  }
		else{
			if(rows.length > 0) {
				req.session.username = rows[0].user_id//username
				req.session.id = rows[0].user_id //DOESNT WORK, PLEASE FIX
      			req.session.loggedin = true;
				console.log("Session username = ", req.session.username)


				res.redirect('/homepage')			
			}
			else{
				console.log("Wrong username or password")
				res.redirect('/')
			}
		}
	})
})
