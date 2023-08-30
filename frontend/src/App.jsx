import './App.css'
import Header from './Header';
import Footer from './Footer';
import Nav from './Nav';
import {Outlet} from 'react-router-dom'
import {useState} from 'react';
import api from './api/axios'


function App() {
  const apiFetch = async(path) => {
    try {
      const response = await api.get("/" + path);
      // console.log("Fetching...")
      // console.log(response);
      // console.log("Done Fetching");
      return response;
    } catch (err){
      console.log(err);
    }
  }

  const apiPut = async(path, data) => {
    try{
      const response = await api.put(path, data);
      return response;
    }catch(err){
      console.log(err);
    }
  }

  const apiDelete = async(path) => {
    try{
      const response = await api.delete(path);
      return response;
    }catch(err){
      console.log(err);
    }
  }

  const apiPost = async(path, data) => {
    try{
      const response = await api.post(path, data);
      return response;
    }catch(err){
      console.log(err);
    }
  }


  return (
    <div className="App">
      <Header />
      <Nav />
      <Outlet context={[apiFetch, apiPut, apiDelete, apiPost]}/>
      <Footer />
    </div>
  )
}

export default App
