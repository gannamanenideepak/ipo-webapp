import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import CompanyList from "./components/CompanyList";
import IPOList from "./components/IPOList";
import Login from "./components/Login";
import AdminStats from "./components/AdminStats";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<CompanyList />} />
        <Route path="/ipos" element={<IPOList />} />
        <Route path="/login" element={<Login />} />
        <Route path="/admin/stats" element={<AdminStats />} />
      </Routes>
    </Router>
  );
}

export default App;
