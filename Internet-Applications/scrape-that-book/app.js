const express = require('express');
const cors = require('cors');
const axios = require('axios');
const cheerio = require('cheerio');
const iconv = require('iconv-lite');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.static('public')); // serve static files from 'public' directory

let allBooks = []; // Stores all book data
let currentIndex = 0; // Tracks the current book to scrape in detail

async function fetchPage(url) {
  try {
    const response = await axios.get(url, {
      responseType: 'arraybuffer'
    });
    const decodedContent = iconv.decode(response.data, 'iso-8859-2'); // Decode from UTF-8
    return decodedContent;
  } catch (error) {
    console.error('Error fetching the page:', error);
    return null;
  }
}

function extractBookLinksAndPrices(html) {
  const $ = cheerio.load(html);
  $('ul li .product-container').each((index, element) => {
    const relativeLink = $(element).find('.product-image a').attr('href');
    const fullLink = `https://www.taniaksiazka.pl${relativeLink}`;
    const price = $(element).find('span.product-price').text().trim();
    allBooks.push({ link: fullLink, price });
  });
}

function extractBookDetailsFromPage(html) {
  const $ = cheerio.load(html);
  let bookDetails = {};
  const title = $('div.product-info h1 span').text().trim();

  let pages = null;
  $('div.book-info-elem').each((index, element) => {
    const label = $(element).find('.book-info-label').text().trim();
    if (label.includes('stron')) {
      const pagesText = $(element).find('.book-info-value').text().trim();
      pages = parseInt(pagesText, 10);
      return false; // Break the loop once the correct element is found
    }
  });

  bookDetails.title = title;
  bookDetails.pages = pages;
  return bookDetails;
}


app.get('/scrape', async (req, res) => {
  if (currentIndex < allBooks.length) {
    const bookBasicData = allBooks[currentIndex];
    const bookPageContent = await fetchPage(bookBasicData.link);
    const bookDetailedData = extractBookDetailsFromPage(bookPageContent);

    const pricePerPage = bookDetailedData.pages ? (parseFloat(bookBasicData.price) / bookDetailedData.pages).toFixed(2) : 'N/A';
    
    const bookData = {
      ...bookBasicData,
      ...bookDetailedData,
      pricePerPage
    };

    currentIndex++;
    res.json(bookData);
  } else {
    res.json({ message: "No more books to scrape" });
  }
});

async function fetchAllBookData() {
  const url = 'https://www.taniaksiazka.pl/nowosci';
  const pageContent = await fetchPage(url);
  extractBookLinksAndPrices(pageContent);
}

// Fetch all book data when the server starts
fetchAllBookData().catch(console.error);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
