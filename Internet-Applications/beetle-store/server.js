const express = require('express');
const session = require('express-session');
const path = require('path');

// Database configuration
const db = require('./db/database');

// Routes
const indexRoutes = require('./routes/index');
const checkoutRoutes = require('./routes/checkout');

const app = express();

// Set up session
app.use(session({
  secret: 'your-generated-secret-key',
  resave: false,
  saveUninitialized: true
}));

// EJS setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// Body parser middleware
app.use(express.urlencoded({ extended: false }));

// Use routes
app.use('/', indexRoutes);
app.use('/checkout', checkoutRoutes);

// Start server
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});

module.exports = app;