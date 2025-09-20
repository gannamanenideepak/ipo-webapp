import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      <Link className="navbar-brand" to="/">IPO App</Link>
      <div className="navbar-nav">
        <Link className="nav-link" to="/">Companies</Link>
        <Link className="nav-link" to="/ipos">IPOs</Link>
        <Link className="nav-link" to="/admin/stats">Admin Stats</Link>
        <Link className="nav-link" to="/login">Login</Link>
      </div>
    </nav>
  );
}

export default Navbar;
