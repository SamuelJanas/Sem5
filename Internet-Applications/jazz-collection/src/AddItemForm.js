import React, { useState } from 'react';

const AddItemForm = ({ onAddItem }) => {
  const [newItem, setNewItem] = useState({});


    const handleChange = (e) => {
        setNewItem({
            ...newItem,
            [e.target.name]: e.target.value
        });
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddItem(newItem);
    }



  return (
    <form>
        <h2>Add New Item</h2>
        <div>
            <label htmlFor="title">Title</label>
            <input type="text" name="title" id="title" onChange={handleChange} />
        </div>
        <div>
            <label htmlFor="artist">Artist</label>
            <input type="text" name="artist" id="artist" onChange={handleChange} />
        </div>
        <div>
            <label htmlFor="year">Year</label>
            <input type="text" name="year" id="year" onChange={handleChange} />
        </div>
        <div>
            <label htmlFor="cover">Cover</label>
            <input type="text" name="cover" id="cover" onChange={handleChange} />
        </div>
        <button type="submit" onClick={handleSubmit}>Add Item</button>
    </form>
  );
};

export default AddItemForm;
