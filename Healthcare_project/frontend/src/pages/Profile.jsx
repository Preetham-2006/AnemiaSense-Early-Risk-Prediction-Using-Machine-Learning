import { useEffect, useState } from "react";
import { Save, LogOut, UserCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import API from "../api";

export default function Profile() {
  const navigate = useNavigate();
  const [form,setForm] = useState({name:"",email:""});
  const [loading,setLoading] = useState(true);
  const [saving,setSaving] = useState(false);
  const [message,setMessage] = useState("");
  const [error,setError] = useState("");

  useEffect(()=>{
    API.get("/profile").then(({data})=>{
      const user=data.user || data;
      setForm({name:user.name||"",email:user.email||""});
    }).catch(err=>setError(err.response?.data?.message||"Unable to load profile."))
      .finally(()=>setLoading(false));
  },[]);

  const save = async(e)=>{
    e.preventDefault(); setSaving(true); setError(""); setMessage("");
    try {
      const {data}=await API.put("/profile",form);
      setForm({name:data.user.name,email:data.user.email});
      localStorage.setItem("user",JSON.stringify(data.user));
      setMessage("Profile updated successfully.");
    } catch(err){setError(err.response?.data?.message||"Unable to update profile.");}
    finally{setSaving(false);}
  };

  const logout=()=>{localStorage.clear();navigate("/login",{replace:true});};

  return <div className="app-shell"><Sidebar/><main className="main"><Topbar/><div className="content">
    <div className="page-heading"><div><span className="eyebrow">ACCOUNT & SECURITY</span><h1>My Profile</h1><p>Manage your patient account and session.</p></div></div>
    {loading ? <div className="card">Loading profile...</div> : <div className="profile-layout">
      <section className="card profile-card">
        <div className="large-avatar"><UserCircle size={42}/></div>
        <div><h2>{form.name || "Patient"}</h2><p>{form.email}</p><span className="status-pill green">Patient Account</span></div>
      </section>
      <form className="card" onSubmit={save}><h2>Personal Information</h2><p className="muted">These details are used for your patient portal.</p>
        <div className="form-grid profile-form"><div className="field"><label>Full Name</label><input value={form.name} onChange={e=>setForm(v=>({...v,name:e.target.value}))} required/></div><div className="field"><label>Email</label><input type="email" value={form.email} onChange={e=>setForm(v=>({...v,email:e.target.value}))} required/></div></div>
        {message&&<div className="success-box">{message}</div>}{error&&<div className="error-box">{error}</div>}
        <button className="primary-button" disabled={saving}><Save size={17}/>{saving?"Saving...":"Save Changes"}</button>
      </form>
      <section className="card danger-card"><h2>Session</h2><p>Sign out from this patient portal on this device.</p><button type="button" className="secondary-button" onClick={logout}><LogOut size={17}/>Log Out</button></section>
    </div>}
  </div></main></div>;
}
