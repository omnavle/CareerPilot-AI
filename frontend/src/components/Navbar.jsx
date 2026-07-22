import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  const linkClass = (path) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      location.pathname === path
        ? "bg-indigo-600 text-white"
        : "text-gray-600 hover:bg-gray-100"
    }`;

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <span className="font-bold text-lg text-indigo-600">CareerPilot AI</span>
        <div className="flex gap-2">
          <Link to="/" className={linkClass("/")}>Home</Link>
          <Link to="/upload" className={linkClass("/upload")}>Upload</Link>
          <Link to="/chat" className={linkClass("/chat")}>Chat</Link>
          <Link to="/history" className={linkClass("/history")}>History</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
