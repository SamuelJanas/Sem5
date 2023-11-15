document.getElementById('scrapeButton').addEventListener('click', async () => {
    const response = await fetch('http://localhost:3000/scrape');
    const book = await response.json();
    addBookToTable(book);
  });
  
function addBookToTable(book) {
    const table = document.getElementById('booksTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    // Add cells for title, link, price, pages, price per page
  }
  
function sortTable() {
    const table = document.getElementById("booksTable");
    const rows = Array.from(table.rows).slice(1); // Skip the header row
  
    rows.sort((a, b) => {
      const pricePerPageA = parseFloat(a.cells[4].textContent) || 0;
      const pricePerPageB = parseFloat(b.cells[4].textContent) || 0;
      return pricePerPageA - pricePerPageB;
    });
  
    rows.forEach(row => table.appendChild(row));
  }
  
document.getElementById('scrapeButton').addEventListener('click', async () => {
    const response = await fetch('http://localhost:3000/scrape');
    const book = await response.json();
    addBookToTable(book);
    sortTable();
  });
  