let mongoose = require('mongoose');

// Homeowners Schema
let homeownerSchema = mongoose.Schema({
	name: String,
	plate_number: String,
	address: String,
	contact_number: String,
	conduction_number: String,
	vehicle_type: String,
	model: String,
	date_registered: Date
});

module.exports = mongoose.model('Homeowner', homeownerSchema);
