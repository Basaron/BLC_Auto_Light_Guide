//TODO: Make sessions using cookies

//TODO: Implement the login system

//TODO: Make a proper website

//TODO: Get data down from the database with foreign keys: https://dba.stackexchange.com/questions/129023/selecting-data-from-another-table-using-a-foreign-key

//TODO: Make comments

//TODO: Tighten up the code

//Libraries
const express = require('express') //For setting up the website
const bodyParser = require('body-parser') //For getting the input data

var mysql = require('mysql') //Connecting to the database
var app = express()

app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended:true}))

var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC",
	database: "BLC"
});


app.listen(3000, () => {
    console.log("Server up and running")
})

app.get('/', (req, res) => {
	res.render('login');
})

app.post('/login', (req, res) => {
	var username = req.body.username
	var password = req.body.password
	//TODO: make hash of password
	var query = 'SELECT * FROM users WHERE username = ? AND psw = ?'
	
	connection.query(query, [username, password], (err, result) => {
		if (err){
			console.log(err);
		  }
		else{
			if(result.length > 0) {
				var user_id = result[0].user_id
				console.log(user_id)
				res.redirect('/homepage')			
			}
			else{
				console.log("Wrong username or password")
				res.redirect('/')
			}
		}
	})
})

app.get('/logout', (req, res) => {
	res.redirect('/');
  })

  
app.get('/homepage', (req, res) => {
	res.render('homepage');
})


function createHash(string_input){
	const hash = crypto.createHash('sha256')
	hash.update(string_input);
	return hash.digest('hex');
  }



