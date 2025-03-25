import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import './App.css'
import Login from '../pages/Login'
import HomePage from '../pages/Home'
import Runs from '../pages/Runs'
function App() {


  return (
    <Router>
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/runs" element={<Runs />} />
        </Routes>
    </Router>
  )
}

export default App
