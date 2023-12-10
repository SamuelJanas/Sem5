const express = require('express');
const router = express.Router();
const db = require('../db/database');

// GET home page with product listings
router.get('/', (req, res) => {
    db.query('SELECT * FROM beetles', (err, products) => {
        if (err) throw err;
        res.render('index', {
            products: products,
            query: req.query // Pass the query parameters to the view
        });
    });
});


// POST route to add product to cart
router.post('/add-to-cart/:id', (req, res) => {
    const productId = parseInt(req.params.id);
    if (!req.session.cart) {
        req.session.cart = [];
    }

    db.query('SELECT * FROM beetles WHERE id = ?', [productId], (err, results) => {
        if (err) throw err;
        if (results.length > 0) {
            const product = results[0];

            if (product.quantity <= 0) {
                // Redirect with a message if the product is out of stock
                return res.redirect('/?message=' + encodeURIComponent(product.name + ' is out of stock'));
            }

            const cartItem = req.session.cart.find(item => item.id === productId);

            if (cartItem) {
                if (cartItem.quantity < product.quantity) {
                    cartItem.quantity++;
                } else {
                    // Redirect with a message if no more of this product can be added
                    return res.redirect('/?message=' + encodeURIComponent('No more ' + product.name + ' available'));
                }
            } else {
                req.session.cart.push({ ...product, quantity: 1 });
            }
        }
        res.redirect('/');
    });
});


module.exports = router;