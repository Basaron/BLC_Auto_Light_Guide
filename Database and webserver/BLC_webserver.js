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


