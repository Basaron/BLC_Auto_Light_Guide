//TODO: Make sessions using cookies

//TODO: Implement the login system

//TODO: Make a proper website

//TODO: Get data down from the database with foreign keys: https://dba.stackexchange.com/questions/129023/selecting-data-from-another-table-using-a-foreign-key

//TODO: Make comments

//TODO: Tighten up the code


const express = require('express')
var app = express()
app.set('view engine', 'ejs');




app.listen(3000, () => {
    console.log("Test!")
})

app.get('/', (req, res) => {
	res.render('test');
})

var mysql = require('mysql');

var connection = mysql.createConnection({
	multipleStatements: true,
    port: '3306',
    host: 'localhost',
	user: "root",
	password: "BLC",
	database: "BLC"
});


