import { LayoutDashboard, Activity, FileText, TrendingUp, Lightbulb, UserCircle, LogOut } from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";

const items = [
  ["/", "Dashboard", LayoutDashboard],
  ["/analyze", "Analyze Report", Activity],
  ["/reports", "My Reports", FileText],
  ["/trends", "Health Trends", TrendingUp],
  ["/recommendations", "Recommendations", Lightbulb],
  ["/profile", "Profile", UserCircle],
];

export default function Sidebar() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login", { replace:true });
  };
  return <aside className="sidebar">
    <div className="brand"><div className="brand-icon">◉</div><div><strong>AnemiaSense</strong><span>Blood Health AI</span></div></div>
    <nav>{items.map(([path,label,Icon])=><NavLink key={path} to={path} className={({isActive})=>isActive?"nav-item active":"nav-item"}><Icon size={19}/><span>{label}</span></NavLink>)}</nav>
    <button className="logout-button" onClick={logout}><LogOut size={18}/>Logout</button>
  </aside>;
}
