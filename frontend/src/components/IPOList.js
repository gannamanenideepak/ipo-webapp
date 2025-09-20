import { useEffect, useState } from "react";
import api from "../services/api";

function IPOList() {
  const [ipos, setIpos] = useState([]);

  useEffect(() => {
    api.get("ipo/").then((res) => {
      setIpos(res.data.results || res.data); // handles pagination
    });
  }, []);

  return (
    <div className="container mt-3">
      <h2>IPOs</h2>
      <ul className="list-group">
        {ipos.map((ipo) => (
          <li key={ipo.id} className="list-group-item">
            {ipo.company.name} — {ipo.status} — Price: {ipo.ipo_price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IPOList;
