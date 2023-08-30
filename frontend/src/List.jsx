import {useEffect, useState} from 'react';
import {isRouteErrorResponse, useOutletContext, useParams} from 'react-router-dom';
import api from './api/axios'
import ListItem from './components/ListItem';

const List = () => {
  const [list, setList] = useState([]);
  const [listItems, setListItems] = useState([]);
  const [targetItem, setTargetItem] = useState();
  const [apiFetch, apiPut, apiDelete, apiPost] = useOutletContext();
  const [isUpdated, setIsUpdated] = useState(false);
  const {listID} = useParams();
  const [formData, setFormData] = useState({name:"", description: "", quantity: 0})

  useEffect (() => {
    const fetchData = async () => {
      const response = await apiFetch('grouplist/' + listID)
      setList(response.data)
      setListItems(response.data.items);
    }
    fetchData();
  }, [])

  useEffect(() => {
    if (isUpdated) {
      const data = targetItem
      apiPut(`/grouplist/${list._id}`, data)
    }
    setIsUpdated(false);
  }, [isUpdated, targetItem])

  // This updates the is_purchased property of the item based on the check of the checkbox
  const handleCheck = (name) => {
    const items = listItems.map( (item) => {
      if (item.name === name){
        return {...item, is_purchased: !item.is_purchased}
      } else {
        return item;
      }
    });
    const targetItem = items.find((item) => item.name === name)
    const updatedList = {...list, items: items}
    setTargetItem(targetItem)
    setList(updatedList)
    setListItems(items)
    setIsUpdated(true)
  }

  const handleDelete = (name) => {
    const path = "/grouplist/" + listID + "/" + name;
    apiDelete(path);
    const updatedList = listItems.filter((item) => item.name !== name);
    setListItems(updatedList);
    // Set the state by finding the item in items and removing it
  }

  const handleChange = (event) => {
    const {name, value} = event.target;
    setFormData((prevFormData) => (
      {...prevFormData, [name]: value}
    ))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const path = "/grouplist/" + listID + "/"
    const updatedListItems = [...listItems, formData]
    apiPost(path, formData)
    setListItems(updatedListItems)
  }

  return (
    <main className="List">
      <h2>{list.name}</h2>
      <ul className='"container'>
        {listItems.map((item, index) => (
          <ListItem item={item} index={index} handleCheck={handleCheck} handleDelete={handleDelete}/>
        ))}
      </ul>
      <br />
      <form onSubmit={handleSubmit}>
        <h3>Add New Item</h3>
        <label htmlFor="name">Name: </label>
        <input type="text" name="name" value={formData.name} onChange={handleChange}/>
        <br />
        <label htmlFor="description">Description: </label>
        <input type="text" name="description" value={formData.description} onChange={handleChange}/>
        <br />
        <label htmlFor="quantity">Quantity: </label>
        <input type="number" name='quantity'value={formData.quantity} onChange={handleChange}/>
        <br />
        <input type="submit" value="Submit" />
      </form>
    </main>
  )
}

export default List