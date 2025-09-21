import { useEffect, useState } from "react";
import api from "../services/api";

function CompanyList() {
  const [companies, setCompanies] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    // Fetch companies whenever search changes
    api
      .get(`companies/?search=${search}`)
      .then((res) => {
        setCompanies(res.data.results || []); // handle DRF pagination
      })
      .catch((err) => console.error(err));
  }, [search]);

  return (
    <div className="container mt-4">
      <h2>Companies</h2>

      {/* Search Input */}
      <input
        type="text"
        className="form-control mb-3"
        placeholder="Search companies..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* Company List */}
      <ul className="list-group">
        {companies.map((c) => (
          <li key={c.id} className="list-group-item d-flex align-items-center">
            {c.logo ? (
              <img
                src={`http://127.0.0.1:8000${c.logo}`}
                alt="logo"
                className="me-3 rounded"
                width="40"
                height="40"
              />
            ) : (
              <span className="me-3">📄</span> // fallback if no logo
            )}
            {c.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CompanyList;
