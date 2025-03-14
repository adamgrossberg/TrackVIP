import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import axios from "axios"
import './App.css'
import Login from '../components/Login'

function App() {

//TODO: 
// 1. move the api call logic to a different page - test video upload logic
// 2. create basic login logic
// 3. create homepage:

//   const [inputApiCall, setApiCall] = useState("");
//   const [responseData, setResponseData] = useState(null);
//   const getCustomersData = () => {
//     axios
//         .get("http://127.0.0.1:8000${inputApiCall}")
//         .then(response => setResponseData(response.data))
//         .catch(error => console.log(error));
//     };
//     getCustomersData();

  return (
    <Router>
        <Routes>
            <Route path="/login" element={<Login />} />
        </Routes>
    </Router>
    
    //   <div className="card">
    //   <input
    //       type="text"
    //       value={inputValue}
    //       onChange={(e) => setInputValue(e.target.value)} // Update state on change
    //       placeholder="Enter text"
    //     />
    //     <button onClick={fetchData}>Send Request</button>
    //   </div>
    //   {responseData && <p>Response: {responseData}</p>}
    // </> */
  )
}

export default App
