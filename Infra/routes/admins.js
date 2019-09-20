const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

router = express.Router();

// connect database
mongoose.connect('mongodb://localhost/test', {useNewUrlParser: true});
let db = mongoose.connection;

db.once('open', () => {
	console.log("connected to mongodb");
})

db.on('error', (err) => {
	console.log(err);
});

// load log model
Admins = require('../models/admin');

/*
* @route  GET
* @desc	  Show all admins
* @access Public
*/
router.get("/", (req, res) => {
	Admins.find({}, (err, admins) => {
		if (err) console.log("ERROR");
		res.render('admin', {admins:admins});
		//res.json(admins);
	})
});	

/*
* @route  GET
* @desc	  Form for adding admin
* @access Public
*/
router.get("/add", (req, res) => {
	res.render('add_admin', {title: 'Add Admin'});
});

/*
* @route  POST
* @desc	  Add admin
* @access Public
*/
router.post("/add", (req, res) => {
	//res.json("added admin!");
	if (req.body.password != req.body.confirm) {
		req.flash('danger', 'Passwords do not match');
		res.redirect('/admins/add');
	}

	Admins.findOne({username:req.body.username}, (err, admin) => {
		if (admin) {
			req.flash('danger', 'Admin already exists');
			res.redirect('/admins/add');
		}
		else {
			let add = new Admins({
				name: req.body.name,
				username: req.body.username,
				password: req.body.password
			});

			// hash password
			bcrypt.genSalt(10, (err, salt) => {
				bcrypt.hash(add.password, salt, (err, hash) => {
					if (err) console.log(err);
					add.password = hash;
					add.save((err) => {
						if (err) {
							console.log(err);
							return;
						}
						else {
							req.flash('success', 'Admin created!');
							res.redirect('/');
						}
					});
				});
			});
		}
	});
});

module.exports = router;
