import { useEffect, useState } from "react";
import api from "../services/api";

function IPOList() {
  const [ipos, setIpos] = useState([]);
  const [status, setStatus] = useState("");

  useEffect(() => {
    api
      .get(`ipo/?status=${status}`)
      .then((res) => setIpos(res.data.results || []))
      .catch((err) => console.error(err));
  }, [status]);

  return (
    <div className="container mt-4">
      <h2>IPO List</h2>

      {/* Filter Dropdown */}
      <select
        className="form-select mb-3"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <option value="">All IPOs</option>
        <option value="upcoming">Upcoming</option>
        <option value="ongoing">Ongoing</option>
        <option value="completed">Completed</option>
      </select>

      {/* IPO Cards Grid */}
      <div className="row">
        {ipos.map((ipo) => (
          <div className="col-md-4 mb-3" key={ipo.id}>
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{ipo.company_name}</h5>
                <p className="card-text">
                  Price: ₹{ipo.price_band} <br />
                  Date: {ipo.start_date} → {ipo.end_date}
                </p>

                {/* IPO Logo */}
                {ipo.logo && (
                  <img
                    src={`http://127.0.0.1:8000${ipo.logo}`}
                    alt="IPO logo"
                    width="50"
                    className="mb-2"
                  />
                )}

                <br />

                {/* Download Prospectus */}
                {ipo.document && (
                  <a
                    href={`http://127.0.0.1:8000${ipo.document}`}
                    className="btn btn-sm btn-outline-primary"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download PDF
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default IPOList;
