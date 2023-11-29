import React, { useState, useMemo } from 'react';
import ItemList from './ItemList';
import AddItemForm from './AddItemForm';
import initialData from './data.json';

function App() {
  const [items, setItems] = useState(initialData);
  const [showForm, setShowForm] = useState(false);
  const [sortMethod, setSortMethod] = useState('none');
  const [searchQuery, setSearchQuery] = useState('');

  const handleUpdateItem = (updatedItem) => {
    setItems(items.map(item => item.id === updatedItem.id ? updatedItem : item));
  };

  const handleAddItem = (newItem) => {
    setItems([...items, { ...newItem, id: items.length + 1 }]);
    setShowForm(false); // Hide form after adding an item
  };

  const handleDeleteItem = (itemId) => {
    setItems(items.filter(item => item.id !== itemId));
  };

  const toggleForm = () => {
    setShowForm(!showForm);
  };

  // Sorting logic
  const filteredAndSortedItems = useMemo(() => {
    const filtered = items.filter(
      item => item.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      item.artist.toLowerCase().includes(searchQuery.toLowerCase()) || 
      item.year.toString().includes(searchQuery)
      );

    switch (sortMethod) {
      case 'year-asc':
        return filtered.sort((a, b) => a.year - b.year);
      case 'year-desc':
        return filtered.sort((a, b) => b.year - a.year);
      case 'alpha':
        return filtered.sort((a, b) => a.title.localeCompare(b.title));
      default:
        return filtered;
    }
  }, [items, sortMethod, searchQuery]);

  return (
    <div className="App">
      <header className="app-header">
        <h1>My Jazz Album Collection</h1>
        <div className="header-controls">
          <button onClick={toggleForm} className="toggle-form-button">
            {showForm ? 'Hide Form' : 'Add New Album'}
          </button>
          <div className="sorting-container">
            <select onChange={(e) => setSortMethod(e.target.value)} className="sorting-dropdown">
              <option value="none">No Sorting</option>
              <option value="year-asc">Year (Ascending)</option>
              <option value="year-desc">Year (Descending)</option>
              <option value="alpha">Alphabetical</option>
            </select>
          </div>
          <input
            type="text"
            placeholder="Search..."
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>
      </header>
      {showForm && <AddItemForm onAddItem={handleAddItem} />}
      <ItemList
        items={filteredAndSortedItems}
        onUpdateItem={handleUpdateItem}
        onDeleteItem={handleDeleteItem}
        searchQuery={searchQuery}
      />
    </div>
  );
}

export default App;