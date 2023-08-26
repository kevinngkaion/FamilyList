import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Error from './Error.jsx'
import './index.css'
import {createBrowserRouter, RouterProvider } from 'react-router-dom'
import Login from './Login.jsx'
import User from './User.jsx'
import Home from './Home.jsx'
import Group from './Group.jsx'
import List from './List.jsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
    errorElement: <Error/>,
    children: [
      {
        path: "login",
        element: <Login/>,
      },
      {
        path: "user",
        element: <User/>,
      },
      {
        path: "home",
        element: <Home/>,
      },
      {
        path: "group",
        element: <Group/>,
      },
      {
        path: "List",
        element: <List/>,
      }
    ]
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
