
const ItemInfo = ({item}) => {
    return (
    <div className="ItemInfo">
        <div className="item-name">{item.name}</div>
        <div className="item-description">notes: {item.description}</div>
        <div className="item-quantity">qty: {item.quantity}</div>
    </div>
  )
}

export default ItemInfo