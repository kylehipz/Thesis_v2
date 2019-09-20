const express = require('express');
const mongoose = require('mongoose');
let router = express.Router();

// Database connection
mongoose.connect('mongodb://localhost/test');
let db = mongoose.connection;

db.once('open', () => {
	console.log("connected to mongodb");
});

db.on('error', (err) => {
	console.log(err);
});

// Load models
let Admins = require('../models/admin');


module.exports = router;
