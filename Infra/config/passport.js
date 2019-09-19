const LocalStrategy = require('passport-local').Strategy;
const Admin = require('../models/admin');

const bcrypt = require('bcryptjs');

module.exports = (passport) => {
	passport.use(new LocalStrategy((username, password, done) => {
		Admin.findOne({username:username}, (err, admin) => {
			if (err) throw err;
			if (!admin) {
				return done(null, false, {message: 'No admin exists'});
			}

			bcrypt.compare(password, admin.password, (err, isMatch) => {
				if (err) throw err;
				if (isMatch) {
					return done(null, admin);
				}
				else {
					return done(null, false, { message: 'Wrong password' });
				}
			});
		});
	}));

	passport.serializeUser((user, done) => {
		done(null, user.id);
	});

	passport.deserializeUser((id, done) => {
		Admin.findById(id, (err, admin) => {
			done(err, admin);
		});
	});
};
