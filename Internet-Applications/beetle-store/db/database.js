const mysql = require('mysql');

// Create a MySQL pool
const pool = mysql.createPool({
  connectionLimit: 10,
  host: 'localhost',
  user: 'root', // username
  password: 'rootROOT', // I know .env exists, it's fine.
  database: 'beetle-store'
});

// Export the pool
module.exports = pool;
