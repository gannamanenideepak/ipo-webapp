import { useEffect, useState } from "react";
import api from "../services/api";

function AdminStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("admin/stats/").then((res) => {
      setStats(res.data);
    }).catch(() => alert("Unauthorized or expired token"));
  }, []);

  if (!stats) return <p>Loading...</p>;

  return (
    <div className="container mt-3">
      <h2>Admin Stats</h2>
      <ul className="list-group">
        <li className="list-group-item">Total Companies: {stats.total_companies}</li>
        <li className="list-group-item">Total IPOs: {stats.total_ipos}</li>
        <li className="list-group-item">Total Users: {stats.total_users}</li>
      </ul>
    </div>
  );
}

export default AdminStats;
