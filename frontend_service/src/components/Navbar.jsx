import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <Link to="/">Dashboard</Link>
      <Link to="/market">Market</Link>
      <Link to="/system">System</Link>
    </div>
  );
}