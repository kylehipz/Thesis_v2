const express = require('express');
const mongoose = require('mongoose');
let router = express.Router();

// connect database
mongoose.connect('mongodb://localhost/test');
let db = mongoose.connection;

function isAuthenticated(req, res, next) {
	if (!req.session.user) {
		req.flash('danger', 'You need to log in first!');
		res.redirect('/');
	}

	next();
};

db.once('open', () => {
	console.log("connected to mongodb");
})

db.on('error', (err) => {
	console.log(err);
});

// load log model
Logs = require('../models/log');
Homeowners = require('../models/homeowner');

/*
* @route  GET
* @desc	  Get all logs
* @access Public
*/
router.get("/", (req, res) => {
	Logs.find({}, (err, logs) => {
		if (err)
			console.log("ERROR!");

		res.render('logs', { logs:logs });

		//res.json(logs);
	});
});

/*
* @route  GET
* @desc	  Ajax for logs
* @access Public
*/
router.get("/ajax_logs", (req, res) => {
	Logs.find({}).sort({date_recorded:-1}).exec((err, logs) => {
		res.json(logs);
	});
});



/*
* @route  GET
* @desc	  Get a specific log
* @access Public
*/
router.get("/:id", (req, res) => {
	Logs.findOne({image_path:req.params.id}).then((log) => {
		res.render('see_log', { log:log });
		//res.json(log);
	})
	//res.json({id:req.params.id});
});

module.exports = router;
