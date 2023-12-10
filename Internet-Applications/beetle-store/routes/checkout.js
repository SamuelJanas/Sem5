const express = require('express');
const router = express.Router();
const db = require('../db/database');

// GET checkout page
router.get('/', (req, res) => {
    res.render('checkout', { cart: req.session.cart || [] });
});


router.post('/cancel', (req, res) => {
    req.session.cart = [];
    res.redirect('/?message=Purchase+Cancelled');
});

// POST route to finalize purchase
router.post('/finalize', (req, res) => {
    if (!req.session.cart || req.session.cart.length === 0) {
        return res.redirect('/checkout?message=Your+cart+is+empty');
    }

    // Get a connection from the pool
    db.getConnection((err, connection) => {
        if (err) {
            throw err; // not connected!
        }

        // Start a transaction
        connection.beginTransaction(err => {
            if (err) {
                connection.release();
                throw err;
            }

            let queriesCompleted = 0;

            req.session.cart.forEach(item => {
                connection.query('UPDATE beetles SET quantity = quantity - ? WHERE id = ? AND quantity >= ?',
                    [item.quantity, item.id, item.quantity], (err, result) => {
                        if (err) {
                            return connection.rollback(() => {
                                connection.release();
                                throw err;
                            });
                        }

                        if (result.affectedRows === 0) {
                            // Rollback if the item quantity couldn't be updated
                            return connection.rollback(() => {
                                connection.release();
                                res.redirect('/?message=Not+enough+stock+for+' + encodeURIComponent(item.name));
                            });
                        }

                        queriesCompleted++;
                        if (queriesCompleted === req.session.cart.length) {
                            // Commit the transaction when all queries are completed
                            connection.commit(err => {
                                if (err) {
                                    return connection.rollback(() => {
                                        connection.release();
                                        throw err;
                                    });
                                }

                                console.log('Purchase finalized successfully');
                                req.session.cart = []; // Clear the cart
                                connection.release(); // Release the connection back to the pool
                                res.redirect('/?message=Purchase+Successful');
                            });
                        }
                    }
                );
            });
        });
    });
});


module.exports = router;