const express = require('express');
const app = express();
const port = 3000;
const cors = require('cors');


app.use(cors());
app.use(express.static('public')); // serve static files from 'public' directory

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

app.get('/scrape', async (req, res) => {
    const url = 'https://www.taniaksiazka.pl/bestsellery';
    const pageContent = await fetchPage(url);
    const books = extractBookDetails(pageContent);

    if (currentIndex < books.length) {
        const book = books[currentIndex];
        currentIndex++;
        res.json(book);
      } else {
        res.json({ message: "No more books to scrape" });
      }
  });

  