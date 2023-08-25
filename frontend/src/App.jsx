import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './Header'
import Content from './Content'
import Footer from './Footer'
import {useCookies} from 'react-cookie'

function App() {
  const [cookies, setCookie, removeCookie] = useCookies([]);
  return (
    <div className='App'>
      <Header />
      <Content cookies={cookies} setCookie={setCookie} removeCookie={removeCookie} />
      <Footer />
    </div>
  );
}

export default App
