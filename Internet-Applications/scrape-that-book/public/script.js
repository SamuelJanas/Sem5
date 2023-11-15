
function addBookToTable(book) {
    const table = document.getElementById('booksTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
  
    // Add cells for title, link, price, pages, price per page
    const titleCell = newRow.insertCell();
    titleCell.textContent = book.title;
  
    const linkCell = newRow.insertCell();
    const link = document.createElement('a');
    link.setAttribute('href', book.link);
    link.textContent = 'View';
    linkCell.appendChild(link);
  
    const priceCell = newRow.insertCell();
    priceCell.textContent = book.price;
  
    const pagesCell = newRow.insertCell();
    pagesCell.textContent = book.pages;
  
    const pricePerPageCell = newRow.insertCell();
    pricePerPageCell.textContent = book.pricePerPage;

    sortTableByPricePerPage();
  }
  
function sortTableByPricePerPage() {
    const table = document.getElementById('booksTable').getElementsByTagName('tbody')[0];
    let rows = Array.from(table.rows);
  
    rows.sort((rowA, rowB) => {
      let valueA = parseFloat(rowA.cells[4].textContent);
      let valueB = parseFloat(rowB.cells[4].textContent);

      if (isNaN(valueA)) {
        valueA = 1000;
      }
      if (isNaN(valueB)) {
        valueB = 1000;
      }
      return valueA - valueB; // For ascending order, swap valueA and valueB for descending
    });
  
    rows.forEach(row => table.appendChild(row)); // Re-adding sorted rows to the table
  }

document.getElementById('scrapeButton').addEventListener('click', async function(e) {
    console.log("Button clicked"); // This should log once per click
    const response = await fetch('http://localhost:3000/scrape');
    const book = await response.json();
    addBookToTable(book);
  });
  