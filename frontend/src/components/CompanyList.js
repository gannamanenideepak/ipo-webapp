import { useEffect, useState } from "react";
import api from "../services/api";

function CompanyList() {
  const [companies, setCompanies] = useState([]);

useEffect(() => {
  api.get("/companies/").then((res) => {
    setCompanies(res.data.results || []);  // ✅ handle pagination
  }).catch(err => {
    console.error("Error fetching companies:", err);
    setCompanies([]); // fallback
  });
}, []);

return (
  <div className="container mt-4">
      <h2>Companies</h2>
      <ul className="list-group">
        {companies.map((c) => (
          <li key={c.id} className="list-group-item">
            {c.name}
          </li>
        ))}
      </ul>
    </div>
);
}

export default CompanyList;
