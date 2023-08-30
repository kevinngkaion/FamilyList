import { Link } from "react-router-dom"

const ClickableRow = ({list}) => {
  const listID = list._id;
  return (
    <li key={listID} className="ClickableRow">
        <button>
            <Link to={'/lists/' + listID}>
                <h3>{list.name}</h3>
                <p><i>{list.group.name}</i></p>
            </Link>

        </button>
    </li>
  )
}

export default ClickableRow