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

/********************  Middlewares ************************************************/

// Back button
app.use(function(req, res, next) {
  res.set('Cache-Control', 'no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0');
  next();
});

// Mongodb Database Connection 
mongoose.connect('mongodb://localhost/test', {useNewUrlParser: true});
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

// Passport Middleware
require('./config/passport')(passport);
app.use(passport.initialize());
app.use(passport.session());

app.get('*', function(req, res, next){
  res.locals.user = req.session.user || null;
  next();
});

/********************   End    ************************************************/


// load admin model
let Admins = require('./models/admin.js');

/**************** Use Routes ******************/
let routes = require('./routes');
app.use('/homeowners', ensureAuthenticated, routes.homeowners);
app.use('/logs', routes.logs);
app.use('/admins', routes.admins);
/**************** End Routes ******************/

/**************** Root Routes ****************/

/*
 * @route GET
 * @desc Load login page
 * @access Public
 */
app.get("/", ensureLogin, (req, res) => {
	res.render('login', {title: 'Login'});
});

/*
 * @route POST
 * @desc Authenticate Credentials
 * @access Public
 */
app.post("/", (req, res, next) => {
	passport.authenticate('local', {
		successRedirect: '/dashboard',
		failureRedirect: '/',
		failureFlash: true,
	})(req, res, next);
});

/*
 * @route GET
 * @desc load Dashboard
 * @access Public
 */
app.get("/dashboard", ensureAuthenticated, (req, res) => {
	res.render('dashboard', {title: 'Dashboard'});
});

/*
 * @route GET
 * @desc load Live Feed
 * @access Public
 */
app.get("/live_feed", ensureAuthenticated, (req, res) => {
	res.render('live_feed', {title: 'Live Feed'});
});

/*
* @route  GET
* @desc	  Logout
* @access Public
*/
app.get("/logout", async (req, res) => {
	res.set({
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma' : 'no-cache',
    'Expires' : '0',
	});
	await req.logout();
	await req.flash('Success', 'Successfully logged out!');
	await res.redirect('/');
});

/**************** End Root Routes ****************/

/********** Access Control **********/
function ensureAuthenticated(req, res, next) {
	if (req.isAuthenticated()) {
		return next();
	}
	else {
		req.flash('danger', 'You need to login first!');
		res.redirect('/');
	}
}

function ensureLogin(req, res, next) {
	if (!req.isAuthenticated()) {
		return next();
	}
	else {
		res.redirect('/dashboard');
	}
}
/********** End Access Control **********/

/******** Start Server **********/
app.listen(3000, () => {
	console.log("Server has started!");
});


