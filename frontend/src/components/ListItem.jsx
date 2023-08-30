import ItemInfo from "./ItemInfo";
import { FaTrashCan } from "react-icons/fa6";


const ListItem = ({item, index, handleCheck, handleDelete}) => {
  return (
      <li className="ListItem" key={index}>
          <input type="checkbox" onChange={()=>handleCheck(item.name)} checked={item.is_purchased}/>
          <ItemInfo item={item}/>
          <FaTrashCan onClick={()=> handleDelete(item.name)}>
          </FaTrashCan>
      </li>
  )
}

export default ListItem