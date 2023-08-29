import {useEffect, useState} from 'react';
import {isRouteErrorResponse, useOutletContext} from 'react-router-dom';
import api from './api/axios'
import ListItem from './components/ListItem';

const List = () => {
  const [list, setList] = useState([]);
  const [listItems, setListItems] = useState([]);
  const [targetItem, setTargetItem] = useState();
  const [apiFetch, apiPut] = useOutletContext();
  const [isUpdated, setIsUpdated] = useState(false);

  useEffect (() => {
    const fetchData = async () => {
      const response = await apiFetch('grouplist')
      setList(response.data[0])
      setListItems(response.data[0].items);
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

  return (
    <main className="List">
      <h2>{list.name}</h2>
      <ul className='"container'>
        {listItems.map((item, index) => (
          <ListItem item={item} index={index} handleCheck={handleCheck}/>
        ))}
      </ul>
    </main>
  )
}

export default List