const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const session = require('express-session');
const app = express();
const expressValidator = require('express-validator');
const flash = require('connect-flash');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const passport = require('passport');

// Set EJS template engine
app.set("view engine", "ejs");
app.use(express.static('public'));

// Mongodb Database Connection
mongoose.connect('mongodb://localhost/test');
let db = mongoose.connection;
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Session Middleware
app.set('trust proxy', 1); 
app.use(session({
  secret: 'AKO ANG HARI NG TUGMA!',
  resave: true,
  saveUninitialized: true,
}));

// Bodyparser Middleware
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

// Flash Message Middleware
app.use(flash());
app.use(function (req, res, next) {
  res.locals.messages = require('express-messages')(req, res);
  next();
});

// Load Routes
let routes = require('./routes');

// load admin model
let Admins = require('./models/admin.js');

// Use Routes
app.use('/homeowners', routes.homeowners);
app.use('/logs', routes.logs);
app.use('/admins', routes.admins);

// Passport Middleware
require('./config/passport')(passport);
app.use(passport.initialize());
app.use(passport.session());

app.get('*', function(req, res, next){
  res.locals.user = req.session.user || null;
  next();
});


app.get("/", (req, res) => {
	//if (req.session.user)
		//res.redirect('/dashboard');
	//else 
	res.render('login');
});

app.post("/", (req, res, next) => {
	passport.authenticate('local', {
		successRedirect: '/dashboard',
		failureRedirect: '/',
		failureFlash: true
	})(req, res, next);
});

app.get("/dashboard", (req, res) => {
	//console.log(req.session.user);
	res.render('dashboard');
});

// Live Feed
app.get("/live_feed", (req, res) => {
	res.render('live_feed');
});

app.listen(3000, () => {
	console.log("Server has started!");
});


