import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Droplets, Mail, Lock } from "lucide-react";
import API from "../api";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await API.post("/auth/login", { email, password });
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.response?.data?.message || "Unable to sign in. Check your email and password.");
    } finally { setLoading(false); }
  };

  return <div className="auth-page">
    <div className="auth-card">
      <div className="auth-brand"><Droplets size={28}/><strong>AnemiaSense</strong></div>
      <span className="eyebrow">PATIENT PORTAL</span>
      <h1>Welcome back</h1>
      <p>Sign in to access your blood health dashboard.</p>
      <form onSubmit={submit}>
        <div className="field"><label>Email</label><div className="input-with-icon"><Mail size={17}/><input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" required/></div></div>
        <div className="field"><label>Password</label><div className="input-with-icon"><Lock size={17}/><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter password" required/></div></div>
        {error && <div className="error-box">{error}</div>}
        <button className="primary-button full" disabled={loading}>{loading ? "Signing in..." : "Sign In"}</button>
      </form>
      <div className="auth-footer">Don't have an account? <Link to="/register">Create Account</Link></div>
    </div>
  </div>;
}
