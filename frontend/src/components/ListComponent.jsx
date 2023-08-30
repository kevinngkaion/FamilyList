import ClickableRow from "./ClickableRow"

const ListComponent = ({lists}) => {
    return (
    <div className="ListComponent">
        <h2>Your Lists</h2>
        <hr />
        <ul>
            {lists.map((list) => {
                return (<ClickableRow list={list}/>)
            })}
        </ul>
    </div>
  )
}

export default ListComponent