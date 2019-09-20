let mongoose = require('mongoose');

// logs schema
let logSchema = mongoose.Schema({
	plate_number: String,
	image_path: String,
	entrance: Boolean,
	visitor: Boolean,
	owner: String,
	date_recorded: Date,
	date_day: Number,
	date_month: Number
});

module.exports = mongoose.model('Log', logSchema);
