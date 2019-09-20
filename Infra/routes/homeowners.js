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

// Load homeowners model
let Homeowner = require('../models/homeowner');

/*
* @route  GET
* @desc	  Get list of homeowners
* @access Public
*/
router.get("/", (req, res) => {
	Homeowner.find({}, (err, homeowners) => {
		if (err) console.log(err);
		res.render('homeowners', {title: 'Homeowners', homeowners:homeowners });
	});
});

/*
* @route  GET
* @desc	  Add a homeowner
* @access Public
*/
router.get("/add", (req, res) => {
	//res.json("add a homeowner!!");
	res.render('add_homeowner', {title: 'Add Homeowner'});
});

/*
* @route  GET
* @desc	  Show data of a homeowner
* @access Public
*/
router.get("/:id", (req, res) => {
	res.json("Data of owner"+req.params.id);
});

/*
* @route  POST
* @desc	  Add a homeowner
* @access Public
*/
router.post("/", (req, res) => {
	//console.log(req.body);
	var homeowner = new Homeowner(req.body);
	//res.json(req.body);
	homeowner.date_registered = new Date();
	homeowner.save((err, homeowner) => {
		if (err) 
			req.flash('danger', 'Something went wrong');
		else 
			req.flash('success', 'Successfully added');
		res.redirect('/homeowners');
	})
});

module.exports = router;
