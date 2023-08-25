import { useEffect, useState } from 'react';
import api from './api/axios'

const Content = ({cookies, setCookie, removeCookie}) => {
    const [users, setUsers] = useState([]);
    const token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrZXZpbiIsImlkIjoiNjRlNDBmM2NlM2VjMWE1ZjQ2ZWM2NGEyIiwiZXhwIjoxNjkyODMyMTk2fQ.o9GFI7hF7z3Pwet7eOEpg5qyyFoHE0rqE3hSh5fbpMM"
    
    api.interceptors.request.use(
        config => {
            config.headers.authorization = token;
            return config;
        },
        error => {
            return Promise.reject(error);
        }
    );

    const fetch = async (url) => {
        try {
            const response = await api.get("/".concat(url), {withCredentials: true});
            // setUsers(response.data);
            console.log(response)
        } catch (err) {
            console.log(err);
        }
    }

  return (
    <main>
        <button onClick={() => fetch('user')}>Users</button>
        <br />
        <button onClick={() => fetch('group')}>Groups</button>
        <ul>
            {users.map((user) => (
                <li className="user">
                    <p>{user.fname}</p>
                </li>
            ))}
        </ul>
    </main>
  )
}

export default Content