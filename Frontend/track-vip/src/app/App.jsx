import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import './App.css'
import Login from '../pages/Login'
import HomePage from '../pages/Home'
import Runs from '../pages/Runs'
import CreateRunPage from "../pages/CreateRun"
import Navbar from "../components/Header"
import RunDetails from "../pages/RunDetails"

function App() {


  return (
    <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/runs" element={<Runs />} />
            <Route path="/createrun" element={<CreateRunPage />} />
            <Route path="/runs/:id" element={<RunDetails />} />
        </Routes>
    </Router>
  )
}

export default App
