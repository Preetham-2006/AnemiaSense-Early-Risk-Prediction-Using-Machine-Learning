import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import AnalyzeReport from "./pages/AnalyzeReport";
import Reports from "./pages/Reports";
import Trends from "./pages/Trends";
import Recommendations from "./pages/Recommendations";
import Profile from "./pages/Profile";
import ProtectedRoute from "./components/ProtectedRoute";

function Private({ children }) { return <ProtectedRoute>{children}</ProtectedRoute>; }

export default function App() {
  return <Routes>
    <Route path="/login" element={<Login/>}/>
    <Route path="/register" element={<Register/>}/>
    <Route path="/" element={<Private><Dashboard/></Private>}/>
    <Route path="/analyze" element={<Private><AnalyzeReport/></Private>}/>
    <Route path="/reports" element={<Private><Reports/></Private>}/>
    <Route path="/trends" element={<Private><Trends/></Private>}/>
    <Route path="/recommendations" element={<Private><Recommendations/></Private>}/>
    <Route path="/profile" element={<Private><Profile/></Private>}/>
    <Route path="*" element={<Navigate to="/" replace/>}/>
  </Routes>;
}
