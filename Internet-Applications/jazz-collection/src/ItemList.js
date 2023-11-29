import React from 'react';
import Item from './Item';

const ItemList = ({ items, onUpdateItem, onDeleteItem }) => {
  return (
    <div className="container">
      {items.map(item => (
        <Item key={item.id} item={item} onUpdateItem={onUpdateItem} onDeleteItem={onDeleteItem} />
      ))}
    </div>
  );
};

export default ItemList;