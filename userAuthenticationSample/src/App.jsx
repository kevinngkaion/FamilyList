import { useState } from 'react'
import './App.css'
import Header from './Header';
import Footer from './Footer';
import Group from './Group';
import Home from './Home';
import List from './List';
import User from './User';
import Login from './Login';
import Nav from './Nav';
import { Route, Switch, useHistory } from 'react-router-dom';


function App() {
  return (
    <div className='App'>
      <p>Hello</p>
      {/* <Header />
      <Nav />
      <Home />
      <List />
      <User />
      <Group />
      <Login />
      <Footer /> */}
    </div>
  );
}

export default App
