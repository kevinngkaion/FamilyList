import { Link} from 'react-router-dom'

const Nav = () => {
  return (
    // <div>Hello</div>
    <nav className='Nav'>
      <ul className="nav-list">
        <li className="nav-item">
          <Link to={'home'}>Home</Link>
        </li>
        <li className="nav-item">
          <Link to={'list'}>List</Link>
        </li>
        <li className="nav-item">
          <Link to={'group'}>Group</Link>
        </li>
        <li className="nav-item">
          <Link to={'user'}>User</Link>
        </li>
        <li className="nav-item">
          <Link to={'login'}>Login</Link>
        </li>
      </ul>
    </nav>
  )
}

export default Nav