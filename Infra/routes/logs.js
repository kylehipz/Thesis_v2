const express = require('express');
const mongoose = require('mongoose');
let router = express.Router();

// connect database
mongoose.connect('mongodb://localhost/test', {useNewUrlParser: true});
let db = mongoose.connection;

db.once('open', () => {
	console.log("connected to mongodb");
});

db.on('error', (err) => {
	console.log(err);
});

// load log model
let Logs = require('../models/log');
let Homeowners = require('../models/homeowner');

/*
* @route  GET
* @desc	  Get all logs
* @access Public
*/
router.get("/", (req, res) => {
	Logs.find({}, (err, logs) => {
		if (err)
			console.log("ERROR!");

		res.render('logs', {title: 'Logs', logs:logs });

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
* @desc	  Data for charts
* @access Public
*/
router.get("/charts", async (req, res) => {
	var counts = [];
	for (var i = 0; i < 7; i++) {
		var count = await Logs.countDocuments({date_day:i});
		counts.push(count);
	}
	res.json({"counts":counts});
});

/*
* @route  GET
* @desc	  Get a specific log
* @access Public
*/
router.get("/:id", (req, res) => {
	Logs.findOne({image_path:req.params.id}).then((log) => {
		res.render('see_log', {title: 'Log Image',  log:log });
		//res.json(log);
	})
	//res.json({id:req.params.id});
});


module.exports = router;
