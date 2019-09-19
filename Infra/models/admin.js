let mongoose = require('mongoose');

// admin schema
let adminSchema = mongoose.Schema({
	username: String,
	name: String,
	password: String,
	date_created: Date
});

module.exports = mongoose.model('Admin', adminSchema);
