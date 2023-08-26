import {useEffect, useState} from 'react';
import {useOutletContext} from 'react-router-dom';

const Group = () => {
  const [apiFetch] = useOutletContext();
  const [groups, setGroups] = useState([]);

  useEffect( () => {
    const fetchData = async () => {
      const response = await apiFetch('group');
      setGroups(response.data);
    }

    fetchData();
  }, [])

  return (
    <main>
      <h1>This is the Group page!</h1>
      <table>
        <thead>
          <tr>
            <th colSpan={3}>Table Title</th>
          </tr>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Kevin</td>
            <td>Ngkaion</td>
            <td>Admin</td>
          </tr>
        </tbody>
      </table>
      <br />
      {groups && groups.map((group, index)=> {
        return <p key={index}>{group.name}</p>;
      })}
      <br />
      <button onClick={() => apiFetch('user')}>Button</button>
    </main>
  )
}

export default Group