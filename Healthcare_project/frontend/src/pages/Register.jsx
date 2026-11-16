import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Droplets } from "lucide-react";
import API from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name:"", email:"", password:"" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const change = (key, value) => setForm(v => ({...v, [key]:value}));
  const submit = async (e) => {
    e.preventDefault(); setError(""); setLoading(true);
    try {
      const { data } = await API.post("/auth/register", form);
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/", {replace:true});
    } catch(err) { setError(err.response?.data?.message || "Registration failed."); }
    finally { setLoading(false); }
  };
  return <div className="auth-page"><div className="auth-card">
    <div className="auth-brand"><Droplets size={28}/><strong>AnemiaSense</strong></div>
    <span className="eyebrow">CREATE ACCOUNT</span><h1>Get started</h1>
    <p>Create your patient account to manage your blood reports.</p>
    <form onSubmit={submit}>
      <div className="field"><label>Full Name</label><input value={form.name} onChange={e=>change("name",e.target.value)} placeholder="Your name" required/></div>
      <div className="field"><label>Email</label><input type="email" value={form.email} onChange={e=>change("email",e.target.value)} placeholder="you@example.com" required/></div>
      <div className="field"><label>Password</label><input type="password" value={form.password} onChange={e=>change("password",e.target.value)} placeholder="Minimum 6 characters" minLength={6} required/></div>
      {error && <div className="error-box">{error}</div>}
      <button className="primary-button full" disabled={loading}>{loading?"Creating...":"Create Account"}</button>
    </form>
    <div className="auth-footer">Already have an account? <Link to="/login">Sign In</Link></div>
  </div></div>;
}
