import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './Home'
import Bird from "./Bird";
import './App.css'


function App() {
  return (
    
      <Router>
        <Routes>
          <Route path="/" element={<Home></Home>} />
          <Route path="/bird/:id" element={<Bird></Bird>} />
        </Routes>
      </Router>
    
  )
}

export default App
